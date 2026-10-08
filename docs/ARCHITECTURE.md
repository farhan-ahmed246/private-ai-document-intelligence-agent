# Architecture
n8n -> FastAPI -> parsers/chunker -> Ollama embeddings -> Qdrant. Query follows the reverse retrieval path and sends grounded context to Ollama.
