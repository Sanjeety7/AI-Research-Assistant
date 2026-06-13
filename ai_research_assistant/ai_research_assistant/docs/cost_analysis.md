# Cost Analysis

## Per-Query Cost by Model

Costs are calculated based on an average research query consisting of:
- **Input Context:** ~4,000 tokens (RAG documents + Web results + System prompt)
- **Output:** ~1,000 tokens

| Model | Input Cost / 1M | Output Cost / 1M | Est. Cost / Query |
| --- | --- | --- | --- |
| **Claude 3.5 Sonnet** | $3.00 | $15.00 | **$0.027** |
| **GPT-4o** | $5.00 | $15.00 | **$0.035** |
| **Gemini 1.5 Pro** | $3.50 | $10.50 | **$0.024** |
| **Multi-Model Synthesis*** | - | - | **$0.113** |

*\* Multi-Model runs all three models + a synthesis pass by Claude (approx. 8k input / 1k output for synthesis = $0.024 + $0.035 + $0.027 + $0.039).*

## Monthly Cost Projections

Assuming a mix of 40% Claude, 40% GPT-4o, and 20% Gemini, the average blended cost per query is **$0.0296**.

| Traffic Volume | Daily Cost | Monthly Cost (30 Days) |
| --- | --- | --- |
| **100 Queries / Day** | $2.96 | $88.80 |
| **1,000 Queries / Day** | $29.60 | $888.00 |
| **10,000 Queries / Day** | $296.00 | $8,880.00 |

*Vector database (Pinecone) and hosting will add roughly $50-$100/month at the 10k/day scale.*

## Cost Optimization Strategies

1. **Semantic Caching:**
   - **Strategy:** Implement Redis with semantic hashing (using lightweight embeddings) to serve identical or highly similar queries from cache.
   - **Impact:** Can reduce API calls by 15-30% depending on query repetitiveness, saving up to $2,500/month at high scale.

2. **Model Tiering:**
   - **Strategy:** Route simpler queries (e.g., summarization, basic extraction) to faster, cheaper models like **Claude 3.5 Haiku** or **GPT-4o-mini**.
   - **Impact:** Reduces cost for low-complexity tasks by 90%.

3. **Context Trimming (RAG Optimization):**
   - **Strategy:** Instead of blindly injecting the top 5 chunks (which might total 2,500 tokens), use a lightweight re-ranker to only include the top 2 highly relevant chunks.
   - **Impact:** Halving the input tokens saves ~40% of the total query cost.

4. **Cost Guardrails:**
   - **Strategy:** The backend actively estimates token count before calling the LLM. If `estimated_cost > $0.05`, the system can warn the user or enforce truncation.
