# ShopSmart AI — RAG-powered Shopping Assistant

A full-stack Retrieval-Augmented Generation (RAG) application that lets users search a product catalog using natural language instead of filters or exact keywords. Built from scratch — no LangChain — to understand and demonstrate how RAG actually works under the hood.

**Live demo:** [shop-smart-frontend-ecru.vercel.app](https://shop-smart-frontend-ecru.vercel.app)
**Backend API:** [vishroy-shopsmart-ai-backend.hf.space](https://vishroy-shopsmart-ai-backend.hf.space)

---

## What it does

Instead of filtering by brand, price, or category, users can type something like *"comfortable shoes for office under ₹5000"* and the assistant retrieves the most relevant products from the catalog and generates a natural-language recommendation grounded in that data — not made up by the LLM.

## How RAG works in this project

```
User query
    ↓
Embedding model converts text → 384-dim vector
    ↓
ChromaDB performs cosine similarity search
    ↓
Top-k relevant products retrieved
    ↓
Retrieved products + original query packed into a prompt
    ↓
Groq (Llama 3.3 70B) generates a grounded, natural-language answer
    ↓
Response returned to the user
```

This pipeline was built manually (no LangChain) to understand each stage — retrieval, augmentation, and generation — before reaching for a framework.

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite) |
| Backend | FastAPI |
| Vector database | ChromaDB |
| Embedding model | `paraphrase-MiniLM-L3-v2` (sentence-transformers) |
| LLM | Groq — Llama 3.3 70B Versatile |
| Frontend hosting | Vercel |
| Backend hosting | Hugging Face Spaces (Docker) |

## Repositories

This project is split across two repos:

| Repo | Contains |
|---|---|
| [ShopSmart-AI](https://github.com/VishRoy/ShopSmart-AI) | FastAPI backend, RAG pipeline, ChromaDB indexing |
| [ShopSmart-Frontend](https://github.com/VishRoy/ShopSmart-Frontend) | React (Vite) frontend |

### Backend structure

```
ShopSmart-AI/
├── main.py              # FastAPI app and /search endpoint
├── rag_pipeline.py      # Retrieval, augmentation, generation logic
├── data/
│   └── products.csv     # Product catalog
├── Dockerfile
└── requirements.txt
```

### Frontend structure

```
ShopSmart-Frontend/
├── src/
│   ├── App.jsx
│   └── App.css
└── package.json
```

## Running locally

**Backend** (`ShopSmart-AI` repo):
```bash
git clone https://github.com/VishRoy/ShopSmart-AI
cd ShopSmart-AI

python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add a .env file with:
# GROQ_API_KEY=your_key_here

uvicorn main:app --reload
```

**Frontend** (`ShopSmart-Frontend` repo):
```bash
git clone https://github.com/VishRoy/ShopSmart-Frontend
cd ShopSmart-Frontend

npm install

# Add a .env file with:
# VITE_API_URL=http://127.0.0.1:8000

npm run dev
```

## API

**POST** `/search`

Request:
```json
{ "query": "shoes for gym" }
```

Response:
```json
{
  "query": "shoes for gym",
  "retrieved_products": [
    { "name": "Nike Flex Control", "price": 5499, "category": "Gym" },
    { "name": "Puma Gym Trainer Cross", "price": 3499, "category": "Gym" }
  ],
  "answer": "For gym shoes, I'd recommend..."
}
```

## What's next

This is the bare-bones version of the pipeline, built without a framework to understand the fundamentals. Planned next steps:

- Rebuild the pipeline using LangChain and compare the implementation
- Extend into an agent that can use multiple tools (compare products, check discounts, track orders) and decide which to call based on the query

## Why no LangChain (for now)

This version was deliberately built without a framework so that retrieval, augmentation, and generation are each implemented explicitly rather than abstracted away. A LangChain version of the same project is planned as a follow-up to compare the two approaches.
