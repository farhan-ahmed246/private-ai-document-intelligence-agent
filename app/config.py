from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    qdrant_url:str='http://localhost:6333'; qdrant_collection:str='private_documents'; qdrant_api_key:str=''
    ollama_url:str='http://localhost:11434'; ollama_chat_model:str='llama3.2:3b'; ollama_embed_model:str='nomic-embed-text'
    chunk_size:int=900; chunk_overlap:int=150; top_k:int=5; min_score:float=.2; max_upload_mb:int=50; api_token:str=''
    model_config=SettingsConfigDict(env_file='.env',extra='ignore')
settings=Settings()
