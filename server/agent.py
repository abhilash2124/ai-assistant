from dotenv import load_dotenv
import requests
from langchain_core.tools import tool
from langchain_groq import ChatGroq
import os
# ---------------------------
# Tools
# ---------------------------

load_dotenv()

@tool
def recommend_products(query: str) -> str:
    """Recommend products based on user query"""
    res = requests.get(
        "http://127.0.0.1:8000/recommend",
        params={"query": query}
    ).json()

    if not res.get("products"):
        return "No products found"

    names = [p["name"] for p in res["products"]]
    return f"Products: {names}\n{res['answer']}"


@tool
def compare_products(product1: str, product2: str) -> str:
    """Compare two products"""

    res1 = requests.get(
        "http://127.0.0.1:8000/recommend",
        params={"query": product1}
    ).json()

    res2 = requests.get(
        "http://127.0.0.1:8000/recommend",
        params={"query": product2}
    ).json()

    p1 = res1["products"][0]
    p2 = res2["products"][0]

    return f"""
Comparison:

{p1['name']}:
- {p1['description']}
- ₹{p1['price']}

{p2['name']}:
- {p2['description']}
- ₹{p2['price']}

Tell which is better.
"""


# ---------------------------
# LLM (Agent Brain)
# ---------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

tools = [recommend_products, compare_products]

# ---------------------------
# SIMPLE AGENT LOOP (NEW STYLE)
# ---------------------------

def agent(query):
    
    if len(query.strip()) < 3:
        return "Please enter a meaningful query."
    
    print("\n🧠 Thinking...")

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
                return f"\nFinal Answer:\n{result}"

    # If no tool needed
    return f"\nFinal Answer:\n{response.content}"


# ---------------------------
# RUN
# ---------------------------

if __name__ == "__main__":
    while True:
        q = input("\nAsk: ")
        print(agent(q))