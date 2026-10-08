import httpx
from app.config import settings
class QdrantClient:
 def __init__(self): self.base=settings.qdrant_url.rstrip('/');self.h={'api-key':settings.qdrant_api_key} if settings.qdrant_api_key else {}
 async def health(self):
  try:
   async with httpx.AsyncClient(timeout=10) as c:r=await c.get(self.base+'/collections',headers=self.h);return r.is_success
  except httpx.HTTPError:return False
 async def ensure(self,n):
  async with httpx.AsyncClient(timeout=30) as c:
   r=await c.get(f'{self.base}/collections/{settings.qdrant_collection}',headers=self.h)
   if r.status_code==404:
    r=await c.put(f'{self.base}/collections/{settings.qdrant_collection}',json={'vectors':{'size':n,'distance':'Cosine'}},headers=self.h);r.raise_for_status()
 async def upsert(self,points):
  async with httpx.AsyncClient(timeout=60) as c:r=await c.put(f'{self.base}/collections/{settings.qdrant_collection}/points?wait=true',json={'points':points},headers=self.h);r.raise_for_status()
 async def search(self,v,limit):
  async with httpx.AsyncClient(timeout=30) as c:r=await c.post(f'{self.base}/collections/{settings.qdrant_collection}/points/query',json={'query':v,'limit':limit,'with_payload':True},headers=self.h);r.raise_for_status();return r.json()['result']['points']
