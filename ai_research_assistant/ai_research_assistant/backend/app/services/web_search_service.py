# backend/app/services/web_search_service.py
"""Web search integration using DuckDuckGo."""
import asyncio
from duckduckgo_search import DDGS
from app.models.schemas import Source

class WebSearchService:
    """Service to fetch live search results."""
    
    @staticmethod
    async def search(query: str, num_results: int = 5) -> list[Source]:
        """
        Searches DuckDuckGo asynchronously.
        
        Args:
            query (str): Search query.
            num_results (int): Number of top results to return.
            
        Returns:
            list[Source]: A list of web sources.
        """
        def _search():
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=num_results))
                return results
            except Exception as e:
                print(f"DDGS error: {e}")
                return []
                
        # Run blocking search in a thread pool
        results = await asyncio.to_thread(_search)
        
        sources = []
        for i, res in enumerate(results):
            # Assign a pseudo-score: first result gets 0.9, decreasing by 0.05
            score = max(0.5, 0.9 - (i * 0.05))
            sources.append(
                Source(
                    title=res.get("title", "Unknown Title"),
                    content=res.get("body", ""),
                    url=res.get("href", ""),
                    score=score,
                    source_type="web"
                )
            )
        return sources
