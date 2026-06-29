import os
import pandas as pd
import chromadb
from groq import Groq
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize models and clients
print("Loading embedding model...")
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

print("Connecting to Groq...")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="shoes_collection"
)


def index_products():
    # Read CSV
    df = pd.read_csv("data/products.csv")

    # Store each product in vector DB
    for index, row in df.iterrows():
        vector = model.encode(row["description"]).tolist()
        collection.add(
            ids=[row["id"]],
            embeddings=[vector],
            metadatas=[{
                "name": row["name"],
                "price": int(row["price"]),
                "category": row["category"]
            }],
            documents=[row["description"]]
        )
    print(f"✅ {len(df)} products indexed!")


def retrieve(user_query):
    # Convert query to vector
    query_vector = model.encode(user_query).tolist()

    # Search vector DB
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )
    return results


def augment(user_query, retrieved_results):
    # Build context from retrieved products
    context = ""
    for i, metadata in enumerate(retrieved_results["metadatas"][0]):
        context += f"""
Product {i+1}:
Name     : {metadata['name']}
Price    : ₹{metadata['price']}
Category : {metadata['category']}
"""
    # Build final prompt
    prompt = f"""You are a helpful shoe store assistant.
Answer the customer query based ONLY on the products given below.
Do not make up any products or prices.

Available Products:
{context}

Customer Query: {user_query}

Give a helpful and specific recommendation."""

    return prompt


def generate(prompt):
    # Send prompt to LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def rag_pipeline(user_query):
    # Complete RAG pipeline
    retrieved = retrieve(user_query)
    prompt = augment(user_query, retrieved)
    answer = generate(prompt)

    # Get retrieved product names
    products = []
    for metadata in retrieved["metadatas"][0]:
        products.append({
            "name": metadata["name"],
            "price": metadata["price"],
            "category": metadata["category"]
        })

    return {
        "query": user_query,
        "retrieved_products": products,
        "answer": answer
    }


# Load environment variables
load_dotenv()

# Initialize models and clients
print("Loading embedding model...")
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

print("Connecting to Groq...")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="shoes_collection"
)


def index_products():
    # Read CSV
    df = pd.read_csv("data/products.csv")

    # Store each product in vector DB
    for index, row in df.iterrows():
        vector = model.encode(row["description"]).tolist()
        collection.add(
            ids=[row["id"]],
            embeddings=[vector],
            metadatas=[{
                "name": row["name"],
                "price": int(row["price"]),
                "category": row["category"]
            }],
            documents=[row["description"]]
        )
    print(f"✅ {len(df)} products indexed!")


def retrieve(user_query):
    # Convert query to vector
    query_vector = model.encode(user_query).tolist()

    # Search vector DB
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )
    return results


def augment(user_query, retrieved_results):
    # Build context from retrieved products
    context = ""
    for i, metadata in enumerate(retrieved_results["metadatas"][0]):
        context += f"""
Product {i+1}:
Name     : {metadata['name']}
Price    : ₹{metadata['price']}
Category : {metadata['category']}
"""
    # Build final prompt
    prompt = f"""You are a helpful shoe store assistant.
Answer the customer query based ONLY on the products given below.
Do not make up any products or prices.

Available Products:
{context}

Customer Query: {user_query}

Give a helpful and specific recommendation."""

    return prompt


def generate(prompt):
    # Send prompt to LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def rag_pipeline(user_query):
    # Complete RAG pipeline
    retrieved = retrieve(user_query)
    prompt = augment(user_query, retrieved)
    answer = generate(prompt)

    # Get retrieved product names
    products = []
    for metadata in retrieved["metadatas"][0]:
        products.append({
            "name": metadata["name"],
            "price": metadata["price"],
            "category": metadata["category"]
        })

    return {
        "query": user_query,
        "retrieved_products": products,
        "answer": answer
    }


# Index products when file is first run
index_products()
print("✅ RAG Pipeline ready!")

# Index products when file is first run
index_products()
print("✅ RAG Pipeline ready!")
