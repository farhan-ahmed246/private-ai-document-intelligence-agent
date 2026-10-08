import base64
from app.config import settings
from app.chunker import chunk_text
from app.hash_utils import document_id,point_id
from app.parsers.registry import parse_document
from app.ollama_client import OllamaClient
from app.qdrant_client import QdrantClient
async def ingest(name,b64,metadata):
 raw=base64.b64decode(b64,validate=True)
 if len(raw)>settings.max_upload_mb*1024*1024:raise ValueError('File exceeds MAX_UPLOAD_MB')
 text,pages=parse_document(name,raw);chunks=chunk_text(text,settings.chunk_size,settings.chunk_overlap)
 if not chunks:raise ValueError('No readable text extracted')
 o,q=OllamaClient(),QdrantClient();first=await o.embed(chunks[0]);await q.ensure(len(first));doc=document_id(raw);points=[]
 for i,c in enumerate(chunks):
  v=first if i==0 else await o.embed(c);points.append({'id':point_id(doc,i),'vector':v,'payload':{'document_id':doc,'file_name':name,'chunk_id':f'{doc}:{i}','text':c,'metadata':metadata}})
 for i in range(0,len(points),64):await q.upsert(points[i:i+64])
 return {'document_id':doc,'file_name':name,'chunks':len(chunks),'pages':pages,'characters':len(text)}
