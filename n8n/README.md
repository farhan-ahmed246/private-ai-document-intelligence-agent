# n8n A-Z
1. Import document-intelligence-agent.json from Workflow > Import from File.
2. Set PRIVATE_AI_API_URL in n8n when needed. Docker Desktop to host API: http://host.docker.internal:8000. Same Docker network: http://api:8000.
3. Activate the workflow.
4. Ingest webhook accepts JSON: {"file_name":"file.pdf","content_base64":"BASE64","metadata":{"source":"internal"}}.
5. Query webhook accepts {"question":"What does the document say?","top_k":5}.
6. The API uses local Ollama and Qdrant; no cloud LLM key is required.
7. If API_TOKEN is enabled, add Authorization: Bearer TOKEN to both HTTP Request nodes.
