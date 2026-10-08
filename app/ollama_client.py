import httpx
from app.config import settings
class OllamaClient:
 async def health(self):
  try:
   async with httpx.AsyncClient(timeout=10) as c:r=await c.get(settings.ollama_url+'/api/tags'); return r.is_success
  except httpx.HTTPError:return False
 async def embed(self,text):
  async with httpx.AsyncClient(timeout=120) as c:
   r=await c.post(settings.ollama_url+'/api/embed',json={'model':settings.ollama_embed_model,'input':text});r.raise_for_status();return r.json()['embeddings'][0]
 async def chat(self,prompt):
  async with httpx.AsyncClient(timeout=120) as c:
   r=await c.post(settings.ollama_url+'/api/chat',json={'model':settings.ollama_chat_model,'messages':[{'role':'system','content':'Answer only from supplied context. If insufficient, say so.'},{'role':'user','content':prompt}],'stream':False,'options':{'temperature':.1}});r.raise_for_status();return r.json()['message']['content'].strip()
