from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Filter, FieldCondition, MatchValue
from groq import Groq
from dotenv import load_dotenv
import os

import re
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range

# load_dotenv()
load_dotenv("server/.env")

def extract_price(query):
    match = re.search(r'under (\d+)', query.lower())
    if match:
        return int(match.group(1))
    return None


client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Qdrant
# client = QdrantClient(":memory:")
client = QdrantClient(path="qdrant_data")

# User query
query = input("Enter your requirement: ")

# Convert to embedding
query_vector = model.encode(query).tolist()

# Search in Qdrant
# results = client.query_points(
#     collection_name="products", 
#     query=query_vector, 
#     limit=3
#     )
# Detect category from query
category = None
if "phone" in query.lower():
    category = "phone"
elif "laptop" in query.lower():
    category = "laptop"

# Apply filter if detected
if category:
    results = client.query_points(
        collection_name="products",
        query=query_vector,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="category",
                    match=MatchValue(value=category)
                )
            ]
        ),
        limit=3
    )
else:
    results = client.query_points(
        collection_name="products",
        query=query_vector,
        limit=3
    )

print("\n🔍 Recommended Products:\n")

for res in results.points:
    product = res.payload
    print(f"📱 {product['name']}")
    print(f"   💬 {product['description']}")
    print(f"   💰 ₹{product['price']}")
    print(f"   ⭐ Score: {res.score}\n")

client.close()


# Create context from top results
# context = "\n".join([
#     f"{res.payload['name']}: {res.payload['description']}"
#     for res in results.points
# ])
context = "\n".join([res.payload["name"] for res in results.points])

# Create prompt
prompt = f"""
You are an AI product recommendation assistant.

Based on the context below, suggest the best product and explain why.

Context:
{context}

User Query:
{query}

Answer:
"""

# Call LLM
response = client_groq.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("\n🤖 AI Recommendation:\n")
print(response.choices[0].message.content)