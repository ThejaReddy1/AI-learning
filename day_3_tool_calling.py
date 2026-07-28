from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

# Creating client object and assigning the apikey
client = genai.Client(api_key=os.getenv('API_KEY'))

# Defining a simple function to add two numbers
def add_two_numbers(num1: float, num2: float) -> float:
    """Return the sum of two numbers.

    Args:
        num1 (float): First addend.
        num2 (float): Second addend.

    Returns:
        float: The arithmetic sum `num1 + num2`.

    Example:
        >>> add_two_numbers(2, 3)
        5
    """
    return num1 + num2

# Define the function declaration for the tool
function = types.FunctionDeclaration(
    name = "add_two_numbers",
    description = "Add two numbers together",
    parameters_json_schema = {
        'type': 'object',
        'properties': {
            'num1': {
                'type': 'number',
                'description': 'The first number to add, e.g., 5'
            },
            'num2': {
                'type': 'number',
                'description': 'the second number to add, e.g., 3'
            }
        },
        'required': ['num1', 'num2']
    }
)

# Define the tool with the function declaration
tool = types.Tool(function_declarations = [function])

prompt = "what is 46 plus 89?"
system_instruction = "you are a calculator. you can only respond with a function call to add_two_numbers. do not answer in any other way. and always respond with valid JSON only, in the format {\"num1\": float, \"num2\": float, \"sum\": float}. no other text."

# Define a function to call the model
def call(prompt, system=None):

    # Call the model with the prompt and tool, and get the function call response
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents = prompt,
        config = types.GenerateContentConfig(temperature=0, tools=[tool])
    )

    print(response.function_calls[0])  # Print the function call details

    # Create content objects for the user prompt, function call, and function response
    user_prompt_content = types.Content(
        role='user',
        parts=[types.Part.from_text(text = prompt)],
    )

    # Get the function call part and content from the response
    function_call_part = response.function_calls[0]
    function_call_content = response.candidates[0].content

    # Call the function with the arguments from the function call
    try:
        function_result = add_two_numbers(**function_call_part.args)
        function_response = {'result': function_result}
    except (
        Exception
    ) as e:
        function_response = {'error': str(e)}

    # Create a function response part and content from the function response
    function_response_part = types.Part.from_function_response(
        name=function_call_part.name,
        response=function_response,
    )
    function_response_content = types.Content(
        role='user', parts=[function_response_part]
    )


    # Call the model again with the user prompt, function call, and function response, along with the system instruction if provided
    config = types.GenerateContentConfig(temperature=0, tools=[tool])
    if system:
        config.system_instruction=system

    final_response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents = [user_prompt_content, function_call_content, function_response_content],
        config = config
    )
    print(final_response.text)
    print(f"[temp] = {config.temperature}")
    print(f"    token - input: {final_response.usage_metadata.prompt_token_count}, output: {final_response.usage_metadata.candidates_token_count}")

# with out system prompt
call(prompt)

# with system prompt
call(prompt, system_instruction)