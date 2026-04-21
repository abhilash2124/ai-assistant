from dotenv import load_dotenv
import requests
from langchain_core.tools import tool
from langchain_groq import ChatGroq
import os
from groq import Groq

from server.test import products

# Tools

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@tool
def recommend_products(query: str) -> str:
    """Recommend products based on user query"""
    res = requests.get(
        "http://127.0.0.1:8000/recommend",
        params={"query": query}
    ).json()

    return res.get("answer", "No result")


@tool
def compare_products(product1: str, product2: str) -> str:
    """Compare two products and decide the best one"""

    res1 = requests.get("http://127.0.0.1:8000/recommend", params={"query": product1}).json()
    res2 = requests.get("http://127.0.0.1:8000/recommend", params={"query": product2}).json()
    
    if not res1.get("products") or not res2.get("products"):
        return "Could not find products to compare. Please try different names."

    def find_best_match(products, name):
        name = name.lower()
        for p in products:
            if name in p["name"].lower():
                return p
        return products[0]

    p1 = find_best_match(res1["products"], product1)
    p2 = find_best_match(res2["products"], product2)
    prompt = f"""
Compare these two products and decide the BEST one.

Product 1: {p1['name']}
- {p1['description']}
- ₹{p1['price']}

Product 2: {p2['name']}
- {p2['description']}
- ₹{p2['price']}

STRICT FORMAT:

🏆 Best: <product name>

Reasons:
• point 1
• point 2
# Do NOT add extra text.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# LLM (Agent Brain)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

tools = [recommend_products, compare_products]

# SIMPLE AGENT LOOP (NEW STYLE)

def agent(query):
    
    if len(query.strip()) < 3:
        return "Please enter a meaningful query."
    
    if "compare" in query.lower() and "vs" not in query.lower():
        return "Please specify two products like: compare iPhone vs OnePlus"

    # Then continue normal flow
    
    print("\n🧠 Thinking...")
    
    result = None

    response = llm.bind_tools(tools).invoke(query)

    print("\n⚡ Tool Calls:", response.tool_calls)

    # If LLM wants to call tool
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        args = tool_call["args"]

        print("⚡ Calling tool:", tool_name)

        for t in tools:
            if t.name == tool_name:
                result = t.invoke(args)
                return result

    # If no tool needed
        return result or (response.content or "Sorry, I couldn't find an answer.")


# RUN

if __name__ == "__main__":
    while True:
        q = input("\nAsk: ")
        print(agent(q))