# backend/app/models/schemas.py
"""Pydantic schemas for API requests and responses."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Source(BaseModel):
    """Represents a source of information (RAG or Web)."""
    title: str = Field(..., description="Title of the source")
    content: str = Field(..., description="Snippet or full text of the source")
    url: Optional[str] = Field(None, description="URL if web source")
    score: Optional[float] = Field(None, description="Relevance score (0.0 to 1.0)")
    source_type: str = Field(..., description="'rag' or 'web'")

class QueryRequest(BaseModel):
    """Request payload for research query."""
    query: str = Field(..., description="The user's query")
    model_mode: str = Field("auto", description="auto, claude, gpt4o, gemini, or multi")
    routing_mode: str = Field("rag_and_web", description="rag_only, web_only, or rag_and_web")
    history: List[Dict[str, str]] = Field(default_factory=list, description="Previous conversation turns (role, content)")

class QueryResponse(BaseModel):
    """Response payload for research query."""
    answer: str = Field(..., description="The generated answer")
    sources: List[Source] = Field(default_factory=list, description="Sources used to answer")
    confidence: str = Field(..., description="HIGH, MEDIUM, or LOW")
    latency_ms: int = Field(..., description="Time taken to process request in ms")
    token_usage: Dict[str, int] = Field(..., description="Input and output tokens")
    estimated_cost_usd: float = Field(..., description="Estimated cost of the query in USD")
    routed_model: str = Field(..., description="Which model was actually used")
    warnings: List[str] = Field(default_factory=list, description="Any warnings (e.g., high cost)")

class DocumentIngest(BaseModel):
    """Payload to ingest a document into RAG."""
    text: str = Field(..., description="Text content to ingest")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata like source, title, author")
