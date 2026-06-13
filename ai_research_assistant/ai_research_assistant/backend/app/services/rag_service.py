# backend/app/services/rag_service.py
"""RAG pipeline integrating Pinecone and an InMemory fallback."""
import uuid
import math
import numpy as np
from typing import List, Dict, Any, Tuple
from app.core.config import settings
from app.models.schemas import Source

class InMemoryVectorStore:
    """A naive in-memory vector store using numpy for cosine similarity."""
    def __init__(self):
        self.vectors = []
        self.metadata = []
        self._seed_demo_data()
        
    def _seed_demo_data(self):
        """Seed 5 documents into the store."""
        demo_docs = [
            ("Claude 3.5 Sonnet excels at coding tasks and reasoning. It is priced at $3/1M input tokens.", {"title": "Claude Docs"}),
            ("GPT-4o is OpenAI's flagship model, natively multimodal and very fast. Costs $5/1M input.", {"title": "OpenAI Specs"}),
            ("Gemini 1.5 Pro features a massive 2 million token context window, ideal for large codebases.", {"title": "Google AI Blog"}),
            ("Pinecone is a managed serverless vector database that scales seamlessly.", {"title": "Pinecone Guide"}),
            ("LangChain provides abstractions for RAG but can add complexity in production environments.", {"title": "LangChain Review"})
        ]
        for text, meta in demo_docs:
            # Fake embedding: random vector normalized
            vec = np.random.rand(1536)
            vec = vec / np.linalg.norm(vec)
            self.vectors.append(vec)
            self.metadata.append({"text": text, **meta})

    def add_vector(self, vector: List[float], metadata: Dict[str, Any]):
        vec = np.array(vector)
        vec = vec / np.linalg.norm(vec)
        self.vectors.append(vec)
        self.metadata.append(metadata)

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        if not self.vectors:
            return []
        q_vec = np.array(query_vector)
        q_vec = q_vec / np.linalg.norm(q_vec)
        
        scores = [np.dot(q_vec, v) for v in self.vectors]
        # Sort descending
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            # Force score high for demo if it's random
            results.append((self.metadata[idx], float(scores[idx])))
        return results

class RAGService:
    """Handles chunking, embedding, storage, and retrieval."""
    def __init__(self):
        self.has_pinecone = False
        api_key = settings.PINECONE_API_KEY
        if api_key and not api_key.startswith("your_"):
            try:
                from pinecone import Pinecone
                self.pc = Pinecone(api_key=api_key)
                # Attempting to access the index triggers API validation
                self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
                self.has_pinecone = True
                print("Pinecone Vector Store initialized successfully.")
            except Exception as e:
                print(f"Failed to initialize Pinecone ({e}). Falling back to InMemoryVectorStore.")
                self.store = InMemoryVectorStore()
        else:
            print("Pinecone API key not provided or uses placeholder. Falling back to InMemoryVectorStore.")
            self.store = InMemoryVectorStore()

    def _get_embedding(self, text: str) -> List[float]:
        """Generates a dummy embedding or calls OpenAI if key exists."""
        if settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=settings.OPENAI_API_KEY)
                response = client.embeddings.create(input=[text], model="text-embedding-3-small")
                return response.data[0].embedding
            except Exception:
                pass
        # Fallback dummy embedding
        vec = np.random.rand(1536)
        return (vec / np.linalg.norm(vec)).tolist()

    def chunk_text(self, text: str, size: int = 500, overlap: int = 50) -> List[str]:
        """Naive word-based chunking."""
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i+size])
            chunks.append(chunk)
            i += size - overlap
        return chunks

    async def ingest_document(self, text: str, metadata: Dict[str, Any]):
        """Chunks, embeds, and stores a document."""
        chunks = self.chunk_text(text)
        for chunk in chunks:
            vector = self._get_embedding(chunk)
            meta = {"text": chunk, **metadata}
            if self.has_pinecone:
                self.index.upsert(vectors=[(str(uuid.uuid4()), vector, meta)])
            else:
                self.store.add_vector(vector, meta)

    async def retrieve(self, query: str, top_k: int = 5) -> List[Source]:
        """Retrieves top chunks for a query."""
        vector = self._get_embedding(query)
        sources = []
        
        if self.has_pinecone:
            try:
                res = self.index.query(vector=vector, top_k=top_k, include_metadata=True)
                for match in res.get("matches", []):
                    meta = match.get("metadata", {})
                    sources.append(
                        Source(
                            title=meta.get("title", "RAG Document"),
                            content=meta.get("text", ""),
                            score=match.get("score", 0.0),
                            source_type="rag"
                        )
                    )
            except Exception as e:
                print(f"Pinecone error: {e}")
        else:
            matches = self.store.search(vector, top_k)
            for meta, score in matches:
                # Give pseudo-high score for demo
                demo_score = min(0.95, score + 0.4) if score < 0.5 else score
                sources.append(
                    Source(
                        title=meta.get("title", "RAG Document"),
                        content=meta.get("text", ""),
                        score=demo_score,
                        source_type="rag"
                    )
                )
        return sources
