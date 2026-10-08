from app.ollama_client import OllamaClient
from app.qdrant_client import QdrantClient
from app.config import settings
async def retrieve(question,top_k=None):return await QdrantClient().search(await OllamaClient().embed(question),top_k or settings.top_k)
