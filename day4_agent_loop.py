from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

# Creating client object and assigning the apikey
client = genai.Client(api_key=os.getenv('API_KEY'))

prompt = "What is (12 + 8) multiplied by 3?"
system_prompt = "you are a calculator. always respond  final result as JSON only, in the format {\"result\": float}. no other text."

# Defining a simple function to add two numbers
def add_two_numbers(num1: float, num2: float) -> float:
    """Return the sum of two numbers.
    Args:
        num1(float): First addend.
        num2(float): Second added
    
    Returns:
        float: The arithmetic sum `num1 + num2`.
    
    Example:
        >>> add_two_numbers(2, 3)
        5
    """
    return num1 + num2

# Defining a simple multiplication function to multiply two numbers
def multiply_two_numbers(num1: float, num2: float) -> float:
    """Return the product of two numbers.
    
    Args:
        num1(float): First factor.
        num2(float): Second factor.
        
    Returns:
        float: The arithmetic product `num1 * num2`.
    
    Example:
        >>> multiply_two_numbers(2, 3)
        6
    """
    return num1 * num2

# Define the function declaration for the add_two_numbers tool
add_function = types.FunctionDeclaration(
    name="add_two_numbers",
    description="Add two numbers together",
    parameters_json_schema={
        'type': 'object',
        'properties': {
            'num1': {
                'type': 'number',
                'description': 'The first number to add, e.g., 5'
            },
            'num2': {
                'type': 'number',
                'description': 'The second number to add, e.g., 3'
            }
        },
        'required': ['num1', 'num2']
    }
)

multiply_function = types.FunctionDeclaration(
    name="multiply_two_numbers",
    description="Multiply two numbers together",
    parameters_json_schema={
        'type': 'object',
        'properties': {
            'num1': {
                'type': 'number',
                'description': 'The first number to multiply, e.g., 5'
            },
            'num2': {
                'type': 'number',
                'description': 'The second number to multiply, e.g., 3'
            }
        },
        'required': ['num1', 'num2']
    }
)

tool = types.Tool(function_declarations=[add_function, multiply_function])

global history
history = []
# Create content objects for the user prompt, function call, and function response
user_prompt_content = types.Content(
    role='user',
    parts=[types.Part.from_text(text=prompt)]
)
history.append(user_prompt_content)

# Define a function to call the model
def call(history, system=None):

    config = types.GenerateContentConfig(temperature=0, tools=[tool])

    # If a system instruction is provided, set it in the config
    if system:
        config.system_instruction = system
    # Looping until the model provides a final answer
    while True:
        # Call the model with the prompt and tool, and get the function call response
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it",
            contents=history,
            config=config
        )

        print(f"[temp] = {config.temperature}")
        print(f"    token - input: {response.usage_metadata.prompt_token_count}, output: {response.usage_metadata.candidates_token_count}\n")

        if response.function_calls:
            print(response.function_calls[0])  # Print the function call details

            # Get the function call part and content from the response
            function_call_part = response.function_calls[0]
            function_call_content = response.candidates[0].content
            
            # Call the function with the arguments from the function call
            try:
                if function_call_part.name == "add_two_numbers":
                    function_result = add_two_numbers(**function_call_part.args)
                    function_response = {'result': function_result}
                elif function_call_part.name == "multiply_two_numbers":
                    function_result = multiply_two_numbers(**function_call_part.args)
                    function_response = {'result': function_result}
            except (Exception) as e:
                function_response = {'error': str(e)}

            # Create a function response part and content from the function response
            function_response_part = types.Part.from_function_response(
                name=function_call_part.name,
                response=function_response,
            )
            function_response_content = types.Content(
                role='user', parts=[function_response_part]
            )

            history.append(function_call_content) # Add the function call content to the history
            history.append(function_response_content) # Add the function response content to the history
            continue

        else:
            print(f"{response.text}\n")
            del history[1:]  # Clear the history for the next call
            break

# with out system prompt
call(history)

# with system prompt
call(history, system=system_prompt)