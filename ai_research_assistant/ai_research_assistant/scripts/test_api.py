# scripts/test_api.py
"""Script that sends 5 test queries and prints results with routing decisions, sources, and costs."""
import requests
import json
import time

API_URL = "http://localhost:8000/api/research/query"

QUERIES = [
    {"query": "Write a python function to compute the Fibonacci sequence.", "model_mode": "auto", "routing_mode": "rag_only"},
    {"query": "What is the latest news regarding the stock market today?", "model_mode": "auto", "routing_mode": "web_only"},
    {"query": "Compare Claude 3.5 Sonnet and GPT-4o.", "model_mode": "multi", "routing_mode": "rag_only"},
    {"query": "Explain how Pinecone uses HNSW graphs based on my RAG documents.", "model_mode": "auto", "routing_mode": "rag_and_web"},
    {"query": "What are the core differences between LangChain and pure Python for RAG?", "model_mode": "gpt4o", "routing_mode": "rag_only"}
]

def test_queries():
    print("--- Testing API ---")
    for i, req_data in enumerate(QUERIES, 1):
        print(f"\n[{i}/5] Testing Query: '{req_data['query']}'")
        print(f"      Modes -> Model: {req_data['model_mode']}, Routing: {req_data['routing_mode']}")
        
        start_t = time.time()
        try:
            response = requests.post(API_URL, json=req_data)
            latency_script = int((time.time() - start_t) * 1000)
            
            if response.status_code == 200:
                data = response.json()
                print(f"      Status       : SUCCESS ({latency_script}ms script / {data['latency_ms']}ms server)")
                print(f"      Routed Model : {data['routed_model']}")
                print(f"      Confidence   : {data['confidence']}")
                print(f"      Cost         : ${data['estimated_cost_usd']:.5f}")
                print(f"      Sources Used : {len(data['sources'])}")
                for s in data['sources']:
                    print(f"        - [{s['source_type'].upper()}] {s['title']} (Score: {s['score']:.2f})")
                
                print(f"\n      Answer Snippet: {data['answer'][:150]}...")
            else:
                print(f"      FAILED: {response.text}")
        except requests.exceptions.ConnectionError:
            print("      Connection error. Backend not running.")
            break

if __name__ == "__main__":
    test_queries()
