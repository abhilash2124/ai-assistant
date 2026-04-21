from fastapi import FastAPI
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range
from groq import Groq
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import re
from server.agent import agent

# from qdrant_client.models import Range
from pymongo import MongoClient

# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["ai_recommender"]
collection = db["products"]

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load once (IMPORTANT)
model = SentenceTransformer("all-MiniLM-L6-v2")

# client = QdrantClient(":memory:")
client = QdrantClient(path="qdrant_data")

print(client.get_collections())

groq_client =  Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_price(query):
    match = re.search(r'(\d+)\s?k', query.lower())
    if match:
        return int(match.group(1)) * 1000
    return None

# @app.get("/agent")
# def agent_api(query: str):
#     result = agent(query)
#     return {"answer": result}
@app.get("/agent")
def agent_api(query: str):
    result = agent(query)
    
    if "compare" in query.lower():
        return {
            "products": [],
            "answer": result
        }

    # ALSO call recommend to get products
    rec = recommend(query)

    return {
        "products": rec["products"], 
        "answer": result
    }

@app.get("/")
def home():
    return {"message": "AI Product Recommendation API is running 🚀"}

@app.get("/recommend")
def recommend(query: str):
    
    products = list(collection.find({}, {"_id": 0}))

    if not query or query.strip() == "":
        return {
            "products": [],
            "answer": "Please enter a search query."
        }

    query_vector = model.encode(query).tolist()
    price_limit = extract_price(query)
    # Detect category
    category = None
    q = query.lower()

    if "phone" in q or "mobile" in q:
        category = "phone"
    elif "laptop" in q:
        category = "laptop"

    # Search

    # Build filter conditions
    conditions = []

    if category:
        conditions.append(
            FieldCondition(
                key="category",
                match=MatchValue(value=category)
            )
        )

    if price_limit:
        conditions.append(
            FieldCondition(
                key="price",
                range=Range(lte=price_limit)
            )
        )

    # Perform search
    if conditions:
        results = client.query_points(
            collection_name="products",
            query=query_vector,
            query_filter=Filter(must=conditions),
            limit=3
        )
    else:
        results = client.query_points(
            collection_name="products",
            query=query_vector,
            limit=3
        )

    #  Smart fallback
    if len(results.points) == 0:
    # Retry without price filter
        # Retry WITHOUT price but KEEP category
        if category:
            fallback_conditions = []
            
            if category:
                fallback_conditions.append(
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category)
                    )
                )
            
            if price_limit:
                fallback_conditions.append(
                    FieldCondition(
                        key="price",
                        range=Range(lte=price_limit)
                    )
                )

            results = client.query_points(
                collection_name="products",
                query=query_vector,
                query_filter=Filter(must=fallback_conditions),
                limit=3
            )

    # Still no results → return message
    if len(results.points) == 0:
        return {
            "products": [],
            "answer": "No matching products found. Try changing your query."
        }
    # Build context
    
    products_data = [
    {
        "name": res.payload["name"],
        "price": res.payload["price"],
        "description": res.payload["description"]
    }
    for res in results.points
]

    prompt = f"""
You are a strict product recommendation system.

IMPORTANT RULES:
- You MUST choose ONLY from the given products list
- DO NOT use any product outside this list
- If you choose outside → it is WRONG
- Be concise

AVAILABLE PRODUCTS:
{products_data}

USER QUERY:
{query}

RESPONSE FORMAT (STRICT):

🏆 Best Product: <EXACT product name from list>

💡 Why this?
• reason 1
• reason 2
• reason 3
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content

    valid_names = [p["name"] for p in products_data]

    # Check if AI cheated
    if not any(name in answer for name in valid_names):
        # fallback → pick first result
        best = products_data[0]["name"]
        answer = f"""
    🏆 Best Product: {best}

    💡 Why this?
    • Best match based on your query
    • Relevant features
    • Good value
    """

    return {
        "products": [res.payload for res in results.points],
        "answer": answer
    }