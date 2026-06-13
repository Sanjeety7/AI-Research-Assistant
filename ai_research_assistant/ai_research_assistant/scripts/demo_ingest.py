# scripts/demo_ingest.py
"""Script that ingests 10 realistic AI research documents into the RAG store via the API."""
import requests
import json

API_URL = "http://localhost:8000/api/ingest/document"

DOCUMENTS = [
    {
        "text": "The Transformer architecture relies entirely on an attention mechanism to draw global dependencies between input and output.",
        "metadata": {"title": "Attention Is All You Need", "author": "Vaswani et al.", "year": 2017}
    },
    {
        "text": "Retrieval-Augmented Generation (RAG) models combine pre-trained parametric and non-parametric memory for language generation.",
        "metadata": {"title": "RAG for Knowledge-Intensive NLP", "author": "Lewis et al.", "year": 2020}
    },
    {
        "text": "Claude 3.5 Sonnet brings state-of-the-art reasoning and coding capabilities, outperforming competitors on major benchmarks.",
        "metadata": {"title": "Anthropic Claude Release Notes", "source": "anthropic.com"}
    },
    {
        "text": "GPT-4o introduces native multimodal capabilities processing text, audio, and images natively in a single model.",
        "metadata": {"title": "OpenAI GPT-4o Launch", "source": "openai.com"}
    },
    {
        "text": "Vector databases like Pinecone use Hierarchical Navigable Small World (HNSW) graphs to perform approximate nearest neighbor searches efficiently.",
        "metadata": {"title": "Vector Databases Explained", "topic": "Infrastructure"}
    },
    {
        "text": "LangChain's abstraction layers simplify the construction of RAG pipelines but can introduce latency overheads in high-performance applications.",
        "metadata": {"title": "LangChain Pros and Cons", "topic": "Frameworks"}
    },
    {
        "text": "Gemini 1.5 Pro features a 2 million token context window, enabling entire codebases to be analyzed in a single prompt.",
        "metadata": {"title": "Google DeepMind Gemini Update", "source": "google.com"}
    },
    {
        "text": "DuckDuckGo provides an anonymous search API that can be queried using the ddgs python library without API keys.",
        "metadata": {"title": "Python Search Libraries", "topic": "Libraries"}
    },
    {
        "text": "When building multi-model architectures, cost tracking is essential. Token estimation can be done naively by dividing character count by 4.",
        "metadata": {"title": "LLM Production Best Practices", "topic": "Engineering"}
    },
    {
        "text": "FastAPI is a modern, fast web framework for building APIs with Python 3.8+ based on standard Python type hints.",
        "metadata": {"title": "FastAPI Documentation", "source": "fastapi.tiangolo.com"}
    }
]

def ingest_all():
    print("Starting ingestion...")
    for i, doc in enumerate(DOCUMENTS, 1):
        try:
            response = requests.post(API_URL, json=doc)
            if response.status_code == 200:
                print(f"[{i}/{len(DOCUMENTS)}] Ingested: {doc['metadata']['title']}")
            else:
                print(f"[{i}/{len(DOCUMENTS)}] Failed: {response.text}")
        except requests.exceptions.ConnectionError:
            print("Connection error. Make sure the backend is running at http://localhost:8000")
            break

if __name__ == "__main__":
    ingest_all()
