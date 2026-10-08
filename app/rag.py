from app.retrieval import retrieve
from app.ollama_client import OllamaClient
async def answer(question,top_k=None):
 results=await retrieve(question,top_k);ctx='\n\n'.join(f'[SOURCE {i+1}] {p.get("payload",{}).get("text","")}' for i,p in enumerate(results));prompt=f'Question: {question}\n\nContext:\n{ctx}\n\nCite sources like [SOURCE 1]. Do not invent facts.';return await OllamaClient().chat(prompt),results
