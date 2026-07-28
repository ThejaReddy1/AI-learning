from google.genai import types
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
client = genai.Client(api_key=api_key)

def call(prompt, temperature):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents = prompt,
        config=types.GenerateContentConfig(temperature=temperature)
    )
    print(f"[temp]={temperature} {response.text}")
    print(f"    tokens -> input: {response.usage_metadata.prompt_token_count}, output: {response.usage_metadata.candidates_token_count}")

prompt = "What is a hash table and why is it fast for lookups?"

for _ in range(3):
    call(prompt, 0) # for deterministic output. with grounding

for _ in range(3):
    call(prompt, 1) # for deep thinking and highest probability randomness.