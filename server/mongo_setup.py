from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create database
db = client["ai_recommender"]

# Create collection
collection = db["products"]

collection.delete_many({})  # Clear existing data

# Sample products
products = [
    # --- SMARTPHONES (Budget to Flagship) ---
    {
        "name": "Redmi A7 Pro 5G",
        "description": "Entry-level smartphone, not suitable for heavy gaming, best for battery life and basic usage",
        "category": "phone",
        "price": 9999,
        "tag": "Best Under 10k"
    },
    {
        "name": "Xiaomi Redmi Note 15 5G",
        "description": "Superb 120Hz AMOLED display and fast 67W charging.",
        "category": "phone",
        "price": 19999,
        "tag": "Best Under 20k"
    },
    {
        "name": "iQOO Z11",
        "description": "Top-tier gaming performance with Dimensity 8500 at a mid-range price.",
        "category": "phone",
        "price": 25990,
        "tag": "Best Under 30k"
    },
    {
        "name": "OnePlus 15",
        "description": "Flagship power, Hasselblad camera, and ultra-fast 100W charging.",
        "category": "phone",
        "price": 69999,
        "tag": "Best Value Flagship"
    },
    {
        "name": "iPhone 16",
        "description": "Premium build with Apple Intelligence and industry-leading video.",
        "category": "phone",
        "price": 69900,
        "tag": "Best Premium Pick"
    },
    {
        "name": "Samsung Galaxy S25",
        "description": "The best compact Android flagship with a stunning Dynamic AMOLED 2X.",
        "category": "phone",
        "price": 56999,
        "tag": "Best Compact Pick"
    },

    # --- LAPTOPS (Budget to Professional) ---
    {
        "name": "Dell Inspiron 15 3530",
        "description": "Reliable Core i3 performance with 512GB SSD for daily student use.",
        "category": "laptop",
        "price": 34990,
        "tag": "Best Under 35k"
    },
    {
        "name": "HP 15-fd Series",
        "description": "Lightweight design with 12GB RAM, perfect for multitasking and office work.",
        "category": "laptop",
        "price": 39990,
        "tag": "Best Value Laptop"
    },
    {
        "name": "Zebronics ZEB-NBC 5S",
        "description": "High-end Core i7 power at an unbeatable price for heavy processing.",
        "category": "laptop",
        "price": 36990,
        "tag": "Performance Budget Pick"
    },
    {
        "name": "ASUS Vivobook 15",
        "description": "Balanced performance with i5 13th Gen and 16GB RAM for smooth workflows.",
        "category": "laptop",
        "price": 44990,
        "tag": "Best Under 45k"
    },
    {
        "name": "MacBook Air M4",
        "description": "Insane battery life and silent performance. The best overall laptop.",
        "category": "laptop",
        "price": 89990,
        "tag": "Best Premium Laptop"
    }
]


# Insert into DB
collection.insert_many(products)

print("✅ Products inserted into MongoDB")