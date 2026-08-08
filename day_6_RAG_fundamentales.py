from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

# Creating client object and assigning the apikey
client = genai.Client(api_key=os.getenv('API_KEY'))

# 1. Your 5 documents - writing them in a list
documents = [
    "The capital of France is Paris. It is known for its art, fashion, and culture.",
    "The Great Wall of China is a historic fortification built to protect against invasions. It stretches over 13,000 miles.",
    "The Amazon Rainforest is the largest tropical rainforest in the world, home to diverse wildlife and plant species. It plays a crucial role in regulating the Earth's climate.",
    "The Pyramids of Giza in Egypt are ancient structures built as tombs for pharaohs. They are considered one of the Seven Wonders of the Ancient World.", 
    "The Pacific Ocean is the largest and deepest ocean on Earth, covering more than 63 million square miles. It is home to a wide variety of marine life."
]

def embed(text):
    """
    Function to create embeddings for given text using GenAI Embeddings API.
    """
    result = client.models.embed_content(model="gemini-embedding-2", contents=text)
    return np.array(result.embeddings[0].values)

def cosine_similarity(vec_a, vec_b):
    """
    Function to calculate cosine similarity between two vectors.
    """
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    return dot_product / (norm_a * norm_b)

# 2. Embed all documents
doc_embeddings = [embed(doc) for doc in documents]

# 3. your question - pick a question related to the documents
question = "What is the capital of France?"
question_embedding = embed(question)

# 4. Compute similarity of question aganist every doc, print all 5 scores
similarities = []
for i,doc in enumerate(doc_embeddings):
    score = cosine_similarity(question_embedding, doc)
    similarities.append((score, documents[i]))
    print(f"doc {i}: {score:.4f} - {documents[i][:50]}...")


# 5. Sort and take top 2
similarities.sort(reverse=True, key=lambda x: x[0])
top_2 =similarities[:2]

# 6. Build agumented prompt and call the model
context = "\n".join([doc for score, doc in top_2])
prompt = f"Answer using only this context:\n{context}\n\nQuestion: {question}\n"

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

print(response.text)

