from pydantic import BaseModel,Field
class Metadata(BaseModel):
    department:str|None=None; source:str|None=None; tags:list[str]=Field(default_factory=list)
class IngestRequest(BaseModel):
    file_name:str; content_base64:str; metadata:Metadata=Field(default_factory=Metadata)
class QueryRequest(BaseModel):
    question:str=Field(min_length=1); top_k:int|None=Field(default=None,ge=1,le=20)
