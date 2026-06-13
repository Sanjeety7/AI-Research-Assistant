# backend/app/services/model_router.py
"""Smart router to pick the best LLM model."""
import re

class ModelRouter:
    """Classifies queries and routes to the appropriate model."""
    
    @staticmethod
    def route_query(query: str, requested_mode: str) -> str:
        """
        Determines which model to use based on requested mode and query content.
        
        Args:
            query (str): The user query.
            requested_mode (str): The requested mode (auto, claude, gpt4o, gemini, multi).
            
        Returns:
            str: The selected model identifier.
        """
        if requested_mode != "auto":
            return requested_mode
            
        query_lower = query.lower()
        
        # Coding -> Claude
        code_keywords = ["code", "python", "javascript", "debug", "function", "script", "api"]
        if any(re.search(rf"\b{kw}\b", query_lower) for kw in code_keywords):
            return "claude"
            
        # Recent news -> Gemini
        news_keywords = ["latest", "news", "today", "recent", "update"]
        if any(re.search(rf"\b{kw}\b", query_lower) for kw in news_keywords):
            return "gemini"
            
        # Comparisons -> Multi-model synthesis
        compare_keywords = ["compare", "vs", "versus", "difference between"]
        if any(re.search(rf"\b{kw}\b", query_lower) for kw in compare_keywords):
            return "multi"
            
        # Default -> GPT-4o
        return "gpt4o"
