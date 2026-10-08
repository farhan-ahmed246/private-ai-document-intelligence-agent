from app.config import settings
def test_defaults(): assert settings.chunk_size>settings.chunk_overlap and settings.top_k>0
