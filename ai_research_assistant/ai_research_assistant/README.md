# AI Research Assistant

A production-quality AI research assistant prototype featuring multi-model routing (Claude, GPT-4o, Gemini), RAG (Retrieval-Augmented Generation) with Pinecone, and live web search.

## Architecture

```text
  [ Frontend (React/Tailwind) ]
           |
      (REST API)
           v
  [ FastAPI Backend ] ----> [ Model Router ]
           |                      |
    +------+------+         +-----+-----+
    |             |         |     |     |
 [ RAG ]     [ Web ]    [Claude] [GPT] [Gemini]
    |             |
[Pinecone]  [DuckDuckGo]
```

## Features

- **Multi-Model Routing:** Smartly routes queries to Claude (coding), GPT-4o, or Gemini (recent news), or uses Multi-Model Synthesis to combine all three.
- **RAG Pipeline:** Ingest documents into Pinecone (with an InMemory fallback) to ground answers in private data.
- **Web Search:** Integrates DuckDuckGo for live internet access.
- **Cost Tracking:** Real-time token counting and cost estimation per query.
- **Redis Caching:** Optional Redis integration to cache responses for 1 hour.
- **Beautiful UI:** React + Tailwind single-page app with dark mode, markdown rendering, and source citations.

## Quick Start

1. **Clone the repository & Set up `.env`**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add your API keys (Anthropic, OpenAI, Gemini)
   ```

2. **Run the Backend (Docker or Local)**
   ```bash
   # Option A: Local Python
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   
   # Option B: Docker
   docker build -t ai-research-assistant .
   docker run -p 8000:8000 --env-file .env ai-research-assistant
   ```

3. **Run the Frontend**
   Simply open `frontend/index.html` in your web browser. No build step required!

## API Reference

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Ingest Document
```bash
curl -X POST http://localhost:8000/api/ingest/document \
  -H "Content-Type: application/json" \
  -d '{"text": "Claude 3.5 Sonnet is a fast and intelligent model.", "metadata": {"source": "anthropic_docs"}}'
```

### Research Query
```bash
curl -X POST http://localhost:8000/api/research/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?", "model_mode": "auto", "routing_mode": "rag_and_web"}'
```

## Tech Stack

| Component | Technology |
| --- | --- |
| Frontend | React 18, Tailwind CSS, Lucide Icons |
| Backend | Python 3.10+, FastAPI, Pydantic |
| LLMs | Anthropic SDK, OpenAI SDK, Google Generative AI |
| Vector DB | Pinecone (with InMemory fallback) |
| Web Search| DuckDuckGo (`ddgs`) |

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
