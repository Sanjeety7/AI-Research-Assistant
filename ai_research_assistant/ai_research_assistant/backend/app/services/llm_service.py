# backend/app/services/llm_service.py
"""Unified LLM client handling Claude, GPT-4o, and Gemini."""
import asyncio
from typing import Dict, Any, List, Tuple
from app.core.config import settings

class LLMService:
    """Service to interact with multiple LLMs."""
    
    # Token prices (Input / Output per 1M)
    PRICES = {
        "claude": (3.0, 15.0),
        "gpt4o": (5.0, 15.0),
        "gemini": (3.5, 10.5)
    }

    def _estimate_tokens(self, text: str) -> int:
        """Naive token estimation (1 token ~= 4 chars)."""
        return len(text) // 4

    def _generate_mock_response(self, prompt: str) -> str:
        """Generates a realistic, context-aware mock response for demo purposes when API keys are missing."""
        import re
        
        # 1. Extract User Query
        query = ""
        query_match = re.search(r"User Query:\s*(.*)", prompt, re.DOTALL)
        if query_match:
            query = query_match.group(1).strip()
            
        # 2. Extract Context Blocks
        context_str = ""
        context_match = re.search(r"Context:\s*(.*?)\s*Conversation History:", prompt, re.DOTALL)
        if context_match:
            context_str = context_match.group(1).strip()
            
        # Parse context sources into dictionaries
        sources = []
        blocks = re.split(r"(\[(?:RAG|WEB)\])", context_str)
        i = 1
        while i < len(blocks):
            src_type = blocks[i].replace("[", "").replace("]", "").strip()
            src_body = blocks[i+1] if i+1 < len(blocks) else ""
            
            title = "Source"
            content = src_body
            if ":" in src_body:
                parts = src_body.split(":", 1)
                title = parts[0].strip()
                content = parts[1].strip()
                
            sources.append({
                "type": src_type,
                "title": title,
                "content": content
            })
            i += 2

        query_lower = query.lower()
        
        # Scenario A: User clicked "Summarize Document" or asked for summary
        is_summary = any(kw in query_lower for kw in ["summarize", "summary", "overview", "key points"])
        
        if is_summary:
            doc_sources = [s for s in sources if s["content"] and "Seed" not in s["title"] and "demo" not in s["content"].lower()]
            if not doc_sources:
                doc_sources = sources
                
            response = "### 📄 Document Analysis & Summary (Demo Mode)\n\n"
            response += "Here is a comprehensive summary of the retrieved document context:\n\n"
            
            for s in doc_sources[:5]:
                sentences = re.split(r"(?<=[.!?])\s+", s["content"])
                summary_snippet = " ".join(sentences[:2])
                response += f"- **{s['title']}** ({s['type']}): {summary_snippet}\n"
                
            response += "\n---\n*💡 **Note:** This response was simulated locally using your uploaded documents and web contexts because no live AI API keys are configured in your `.env` file.*"
            return response

        # Scenario B: User asked a pricing or model comparison question
        is_comparison = any(kw in query_lower for kw in ["compare", "comparison", "pricing", "cost", "vs", "difference"])
        if is_comparison:
            response = "### 📊 Multi-Model Comparison (Demo Mode)\n\n"
            response += "Based on standard AI model metrics, here is a detailed breakdown of the top LLMs:\n\n"
            
            response += "| Model | Provider | Input Cost / 1M | Output Cost / 1M | Max Context Window | Best Use Case |\n"
            response += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
            response += "| **Claude 3.5 Sonnet** | Anthropic | $3.00 | $15.00 | 200,000 tokens | Coding, complex reasoning, logic |\n"
            response += "| **GPT-4o** | OpenAI | $5.00 | $15.00 | 128,000 tokens | Speed, voice, multimodal interaction |\n"
            response += "| **Gemini 1.5 Pro** | Google | $3.50 | $10.50 | 2,000,000 tokens | Large codebase analysis, video processing |\n\n"
            
            response += "#### Key Insights:\n"
            response += "1. **Cost Efficiency:** Claude 3.5 Sonnet offers the best balance of cost and coding intelligence.\n"
            response += "2. **Context Capacity:** Gemini 1.5 Pro dominates in handling massive files or complex repositories with its 2M context window.\n"
            response += "3. **General Purpose:** GPT-4o is the fastest overall responder for high-throughput applications.\n\n"
            response += "---\n*💡 **Note:** This comparison is loaded from local reference data since live API keys are not set up.*"
            return response

        # Scenario C: Search for keywords in context
        matched_sources = []
        for s in sources:
            words = [w for w in re.split(r'\W+', query_lower) if len(w) > 3]
            if any(w in s["content"].lower() or w in s["title"].lower() for w in words):
                matched_sources.append(s)
                
        if matched_sources:
            response = f"### 🔍 Search Analysis (Demo Mode)\n\n"
            response += f"Here are the findings matched to your query: **\"{query}\"**:\n\n"
            for s in matched_sources[:3]:
                response += f"#### {s['title']} ({s['type']})\n"
                response += f"> {s['content']}\n\n"
            response += "---\n*💡 **Note:** This response was extracted from retrieved local/web contexts since live API keys are not configured in your `.env` file.*"
            return response

        # Scenario D: Default response
        response = f"### 🚀 Welcome to AI Research Assistant (Demo Mode)\n\n"
        response += f"Your query: **\"{query}\"** was processed successfully.\n\n"
        response += f"**How to configure live AI responses:**\n"
        response += f"To enable real LLM generation (via Claude, GPT-4o, or Gemini), please edit your configuration:\n\n"
        response += f"1. Open the file [backend/.env](file:///C:/Users/SANJET%20KUMAR/.gemini/antigravity/scratch/ai_research_assistant/backend/.env).\n"
        response += f"2. Update the API key variables with your actual keys:\n"
        response += f"```env\n" \
                    f"ANTHROPIC_API_KEY=sk-ant-...\n" \
                    f"OPENAI_API_KEY=sk-proj-...\n" \
                    f"GEMINI_API_KEY=AIzaSy...\n" \
                    f"```\n"
        response += f"3. Save the file. The backend will automatically reload and use the live keys!\n\n"
        response += f"**Current RAG Context Available:**\n"
        if sources:
            for s in sources[:3]:
                response += f"- **{s['title']}** ({s['type']}): *{s['content'][:100]}...*\n"
        else:
            response += "- No document content indexed yet. Try uploading a PDF in the sidebar!\n"
            
        return response

    async def call_claude(self, prompt: str) -> Tuple[str, Dict[str, int]]:
        if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY.startswith("your_"):
            return self._generate_mock_response(prompt), {"input": self._estimate_tokens(prompt), "output": 250}
        try:
            from anthropic import AsyncAnthropic
            client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = await client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            ans = response.content[0].text
            usage = {"input": response.usage.input_tokens, "output": response.usage.output_tokens}
            return ans, usage
        except Exception as e:
            return f"Claude Error: {e}", {"input": self._estimate_tokens(prompt), "output": 0}

    async def call_gpt4o(self, prompt: str) -> Tuple[str, Dict[str, int]]:
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("your_"):
            return self._generate_mock_response(prompt), {"input": self._estimate_tokens(prompt), "output": 250}
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            ans = response.choices[0].message.content
            usage = {"input": response.usage.prompt_tokens, "output": response.usage.completion_tokens}
            return ans, usage
        except Exception as e:
            return f"GPT-4o Error: {e}", {"input": self._estimate_tokens(prompt), "output": 0}

    async def call_gemini(self, prompt: str) -> Tuple[str, Dict[str, int]]:
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY.startswith("your_"):
            return self._generate_mock_response(prompt), {"input": self._estimate_tokens(prompt), "output": 250}
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            # Run blocking call in thread
            def _call():
                resp = model.generate_content(prompt)
                return resp.text, resp.usage_metadata.prompt_token_count, resp.usage_metadata.candidates_token_count
                
            ans, in_tok, out_tok = await asyncio.to_thread(_call)
            usage = {"input": in_tok, "output": out_tok}
            return ans, usage
        except Exception as e:
            return f"Gemini Error: {e}", {"input": self._estimate_tokens(prompt), "output": 0}

    async def generate(self, prompt: str, model_id: str) -> Tuple[str, Dict[str, int], float]:
        """Generates response and calculates cost."""
        if model_id == "claude":
            ans, usage = await self.call_claude(prompt)
        elif model_id == "gpt4o":
            ans, usage = await self.call_gpt4o(prompt)
        elif model_id == "gemini":
            ans, usage = await self.call_gemini(prompt)
        elif model_id == "multi":
            # Multi-model synthesis
            res = await asyncio.gather(
                self.call_claude(prompt),
                self.call_gpt4o(prompt),
                self.call_gemini(prompt),
                return_exceptions=True
            )
            c_ans = res[0][0] if not isinstance(res[0], Exception) else str(res[0])
            g_ans = res[1][0] if not isinstance(res[1], Exception) else str(res[1])
            gm_ans = res[2][0] if not isinstance(res[2], Exception) else str(res[2])
            
            synth_prompt = f"Synthesize these 3 answers into one perfect response:\n\nClaude: {c_ans}\n\nGPT-4o: {g_ans}\n\nGemini: {gm_ans}"
            ans, synth_usage = await self.call_claude(synth_prompt)
            
            # Aggregate usage (approximation for demo)
            total_in = sum(r[1]["input"] for r in res if not isinstance(r, Exception)) + synth_usage["input"]
            total_out = sum(r[1]["output"] for r in res if not isinstance(r, Exception)) + synth_usage["output"]
            usage = {"input": total_in, "output": total_out}
            model_id = "claude" # base cost on claude for simplicity of multi
        else:
            ans, usage = await self.call_gpt4o(prompt)
            model_id = "gpt4o"
            
        in_cost = (usage["input"] / 1_000_000) * self.PRICES.get(model_id, (0,0))[0]
        out_cost = (usage["output"] / 1_000_000) * self.PRICES.get(model_id, (0,0))[1]
        cost = in_cost + out_cost
        
        return ans, usage, cost
