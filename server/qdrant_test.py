# sourcery skip: for-append-to-extend
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import PointStruct, VectorParams, Distance

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sentences
sentences = [
    "I love coding",
    "I enjoy programming",
    "I hate bugs",
    "abhilash is a great person",
    "abhilash likes programming"
]

# Convert to embeddings
embeddings = model.encode(sentences)

# Create Qdrant client
client = QdrantClient(":memory:")

# Create collection
if not client.collection_exists("my_collection"):
    client.create_collection(
        collection_name="my_collection",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

# Prepare points
points = []
for i, vector in enumerate(embeddings):
    points.append(
        PointStruct(
            id=i,
            vector=vector,
            payload={"text": sentences[i]}
        )
    )

# Store data
client.upsert(
    collection_name="my_collection",
    points=points
)

print("✅ Data stored in Qdrant!")

# Querying
query = "coding is fun"

query_vector = model.encode(query)

result = client.query_points(
    collection_name="my_collection",
    query=query_vector,
    limit=2
)

print("\n 🔍 Search results:")
for res in result.points:
    print(res.payload["text"], " | Score:", res.score)