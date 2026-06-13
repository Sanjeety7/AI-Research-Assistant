# backend/app/api/research.py
"""API routes for research queries."""
import time
import asyncio
from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, Source
from app.services.model_router import ModelRouter
from app.services.rag_service import RAGService
from app.services.web_search_service import WebSearchService
from app.services.llm_service import LLMService

router = APIRouter()
rag_service = RAGService()
web_service = WebSearchService()
llm_service = LLMService()

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Processes a research query end-to-end."""
    start_time = time.time()
    
    # 1. Route model
    routed_model = ModelRouter.route_query(request.query, request.model_mode)
    
    # 2. Gather context
    tasks = []
    if request.routing_mode in ["rag_only", "rag_and_web"]:
        tasks.append(rag_service.retrieve(request.query))
    if request.routing_mode in ["web_only", "rag_and_web"]:
        tasks.append(web_service.search(request.query))
        
    results = await asyncio.gather(*tasks)
    
    sources = []
    for res in results:
        sources.extend(res)
        
    # Sort sources by score
    sources.sort(key=lambda x: x.score or 0.0, reverse=True)
    
    # 3. Assemble prompt
    context_str = "\n\n".join([f"[{s.source_type.upper()}] {s.title}: {s.content}" for s in sources])
    history_str = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in request.history[-5:]])
    
    prompt = f"""You are an expert AI Research Assistant. Answer the user's query based ONLY on the provided context. If the context does not contain the answer, say so.
    
Context:
{context_str}

Conversation History:
{history_str}

User Query: {request.query}
"""
    
    # 4. Generate
    try:
        answer, usage, cost = await llm_service.generate(prompt, routed_model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    latency = int((time.time() - start_time) * 1000)
    
    # 5. Confidence scoring
    rag_sources = [s for s in sources if s.source_type == "rag"]
    high_score_rags = len([s for s in rag_sources if (s.score or 0) > 0.7])
    if high_score_rags >= 3:
        confidence = "HIGH"
    elif high_score_rags >= 1:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"
        
    # 6. Cost Guard
    warnings = []
    if cost > 0.05:
        warnings.append(f"High cost warning: This query cost ${cost:.4f}")
        
    return QueryResponse(
        answer=answer,
        sources=sources,
        confidence=confidence,
        latency_ms=latency,
        token_usage=usage,
        estimated_cost_usd=cost,
        routed_model=routed_model,
        warnings=warnings
    )
