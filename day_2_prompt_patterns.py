from google import genai
from google.genai import types
from dotenv import load_dotenv
import os 

load_dotenv()

# api_key = os.getenv('API_KEY')
client = genai.Client(api_key=os.getenv('API_KEY'))

sentence = "Rahul is 29 years old and work as an engineer."

zero_shot_prompt = f"Extract the name and age from this sentence: {sentence}"

few_shot_prompt = """Extract the name and age from the sentence as JSON.
Sentence: "Priya is 34 and works as a designer."
JSON: {"name": "Priya", "age": 34}

Sentence: "Amith, 41, runs a small bakery."
JSON: {"name": "Amith", "age": 41}

Sentence: """+sentence+""" 
JSON:  """

system_instruction = "You are a data extraction engine. Always respond with valid JSON only, in the format {\"name\": str, \"age\": int}. No other text."

def call(prompt, system=None):
    # config_args = {"temperature" : 0}
    config = types.GenerateContentConfig(temperature=0)
    if system:
        # config_args["system_instruction"] = system
        config.system_instruction=system
    # config = types.GenerateContentConfig(**config_args)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents = prompt,
        config = config
    )
    print(response.text)
    # print(f"[temp]= {config_args["temperature"]}")
    print(f"[temp] = {config.temperature}")
    print(f"    token - input: {response.usage_metadata.prompt_token_count}, output: {response.usage_metadata.candidates_token_count}")

print("*"*25)
print("Zero Shot Prompt")
call(zero_shot_prompt)
print("*"*25)
print("Few Shot Prompt")
call(few_shot_prompt)
print("*"*25)
print("System Prompt")
call(sentence,system_instruction)
print("*"*25)