from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import rag_pipeline

# Initialize FastAPI app

app = FastAPI()

# CORS setup

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# Request Model


class QueryRequest(BaseModel):
    query: str

# Root endpoint — test karne ke liye


@app.get("/")
def root():
    return {"message": "ShopSmart AI is running!"}

# Search endpoint — React yahan se data lega


@app.post("/search")
def search(request: QueryRequest):
    result = rag_pipeline(request.query)
    return result
