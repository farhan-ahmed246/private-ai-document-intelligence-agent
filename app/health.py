def status(qdrant:bool,ollama:bool): return {'status':'ok' if qdrant and ollama else 'degraded','qdrant':qdrant,'ollama':ollama}
