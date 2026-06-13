# Architecture Document

## Component Diagram

```text
+-------------------+       +-----------------------+
|                   |       |                       |
|   React Frontend  | <---> |   FastAPI Backend     |
|   (index.html)    | REST  |   (app/main.py)       |
|                   |       |                       |
+-------------------+       +-----------+-----------+
                                        |
                            +-----------v-----------+
                            |                       |
                            |   API Routers         |
                            |   (app/api/*)         |
                            |                       |
                            +-----------+-----------+
                                        |
          +-----------------------------+-----------------------------+
          |                             |                             |
+---------v---------+         +---------v---------+         +---------v---------+
|                   |         |                   |         |                   |
|   RAG Service     |         |   Model Router    |         | Web Search Service|
|                   |         |                   |         |                   |
+---------+---------+         +---------+---------+         +---------+---------+
          |                             |                             |
+---------v---------+         +---------v---------+         +---------v---------+
|                   |         |                   |         |                   |
| Pinecone / Memory |         |   LLM Service     |         |   DuckDuckGo      |
|                   |         |                   |         |                   |
+-------------------+         +---------+---------+         +-------------------+
                                        |
                            +-----------+-----------+
                            |           |           |
                        +---v---+   +---v---+   +---v---+
                        |       |   |       |   |       |
                        |Claude |   | GPT-4o|   |Gemini |
                        |       |   |       |   |       |
                        +-------+   +-------+   +-------+
```

## Data Flow for a Single Query
1. **Request:** Frontend sends `POST /api/research/query` with query text, context history, routing mode, and model preference.
2. **Controller:** `app.api.research` receives the request.
3. **Routing:** `model_router.py` decides which LLM to use based on the user's preference or auto-detection (e.g., code -> Claude).
4. **Context Gathering (Parallel):**
   - If routing mode includes `rag`, the `RAGService` embeds the query and fetches top-k chunks from Pinecone.
   - If routing mode includes `web`, the `WebSearchService` fetches top web results via DuckDuckGo.
   - Both run concurrently via `asyncio.gather`.
5. **Prompt Assembly:** The results from RAG and Web are combined into a system prompt.
6. **LLM Execution:** The `LLMService` calls the target model API (or all 3 for multi-model synthesis).
7. **Response formatting:** Token usage and cost are calculated. A confidence score is generated based on retrieved sources.
8. **Response:** JSON is returned to the client and rendered.

## RAG Pipeline Internals
1. **Ingestion:** Text is chunked into 500-token pieces with 50-token overlap.
2. **Embedding:** Chunks are embedded using `text-embedding-3-small`.
3. **Storage:** Stored in Pinecone with metadata (source, timestamp). If Pinecone is not configured, falls back to `InMemoryVectorStore`.
4. **Retrieval:** Cosine similarity search returns the top 5 chunks.

## Model Routing Decision Tree
- **If User selected "Auto":**
  - Contains code/programming keywords? -> **Claude**
  - Contains keywords like "latest", "today", "news"? -> **Gemini**
  - General reasoning or factual? -> **GPT-4o**
- **If User selected "Multi-model":**
  - Dispatch requests to Claude, GPT-4o, and Gemini simultaneously.
  - Wait for all 3.
  - Dispatch a 4th request to Claude to synthesize the best parts of the 3 answers.
- **Else:** Use user-specified model.

## Scaling Plan
- **10x Traffic:** 
  - Add Redis caching for repeated queries.
  - Run multiple uvicorn workers.
- **100x Traffic:**
  - Move to Kubernetes with Horizontal Pod Autoscaling.
  - Implement a dedicated embedding microservice.
  - Add API Gateway for rate limiting and load balancing.
  - Shift to streaming responses (Server-Sent Events) to prevent timeout on long LLM generations.
