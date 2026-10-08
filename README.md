# Private AI Document Intelligence Agent

A private, self-hosted document intelligence + RAG backend for n8n automation. Documents are parsed locally, embedded with Ollama, stored in Qdrant, and queried with a local Ollama chat model.

## 1. Stack

- Python 3.12 / FastAPI
- Ollama for local embeddings and chat
- Qdrant for vector storage
- Tesseract OCR for images
- n8n for automation/orchestration
- Docker Compose for API + Qdrant

No OpenAI, Anthropic or Gemini API key is required by the default architecture.

## 2. A-Z installation

### Windows / Linux / macOS

Install Docker Desktop and Ollama. Then:

```bash
git clone https://github.com/farhan-ahmed246/private-ai-document-intelligence-agent.git
cd private-ai-document-intelligence-agent
copy .env.example .env
docker compose up -d --build
```

On Linux/macOS replace `copy` with `cp .env.example .env`.

Pull the models on the machine running Ollama:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Verify:

```bash
curl http://localhost:8000/health
curl http://localhost:11434/api/tags
curl http://localhost:6333/collections
```

The API Swagger UI is at `http://localhost:8000/docs`.

## 3. If Ollama is also in Docker

Change `OLLAMA_URL` in `.env` to the Ollama service name, for example `http://ollama:11434`, and make sure the API and Ollama containers share the same Docker network. Pull the two models inside that Ollama container.

## 4. Test ingestion

The API accepts base64 JSON so n8n can send binary files after converting them to base64.

Example:

```json
{
  "file_name": "sample.txt",
  "content_base64": "UHJpdmF0ZSBBSSBzYW1wbGUgcG9saWN5Lg==",
  "metadata": {
    "department": "HR",
    "source": "internal"
  }
}
```

POST it to `http://localhost:8000/v1/ingest`.

Then query:

```json
{
  "question": "What does the sample policy say?",
  "top_k": 5
}
```

POST to `http://localhost:8000/v1/query`.

The query response contains an answer and retrieved source chunks.

## 5. n8n import

1. Open n8n.
2. Go to **Workflows -> Import from File**.
3. Select `n8n/document-intelligence-agent.json`.
4. Save and activate.
5. If n8n runs in Docker Desktop while FastAPI runs on the host, the workflow default URL is `http://host.docker.internal:8000`.
6. If both are Docker containers on the same network, set `PRIVATE_AI_API_URL=http://api:8000`.
7. If n8n runs directly on the host, use `http://localhost:8000`.

The imported workflow exposes:

- `POST /webhook/private-ai-ingest`
- `POST /webhook/private-ai-query`

For ingest, send:

```json
{
  "file_name": "company-policy.pdf",
  "content_base64": "<base64>",
  "metadata": {"department": "HR"}
}
```

For query, send:

```json
{"question":"What is the leave policy?","top_k":5}
```

## 6. Authentication

Authentication is optional. To enable it, set:

```env
API_TOKEN=your-long-random-token
```

Restart the API. Add this HTTP header to n8n:

```
Authorization: Bearer your-long-random-token
```

Never put real secrets in GitHub.

## 7. Supported formats

PDF, DOCX, XLSX, CSV, JSON, TXT, Markdown, LOG and common image formats.

Text PDFs are parsed with pypdf. Images are processed through Tesseract OCR. For scanned PDFs, use a PDF-to-image OCR pipeline if your deployment requires high-quality scanned-PDF OCR; the base parser does not rasterize PDF pages itself.

## 8. Project structure

```
app/                 FastAPI application and RAG logic
app/parsers/         document parsers
app/routes/          HTTP endpoints
scripts/             setup and smoke-test utilities
n8n/                 importable n8n workflow
tests/               automated tests
docs/                architecture/security/operations notes
sample/              sample document
```

## 9. Local development

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Run tests:

```bash
pytest -q
```

## 10. Troubleshooting

**Ollama down:** check `curl http://localhost:11434/api/tags`, model names and `OLLAMA_URL`.

**Qdrant down:** check `curl http://localhost:6333/collections` and Docker logs.

**n8n cannot connect:** use `host.docker.internal` for Docker Desktop host access, or the API container name when both containers share a network.

**No answer:** ingest at least one document and confirm that the ingest request returns a non-zero chunk count.

**Wrong/weak answer:** use a stronger local chat model, improve document quality, adjust `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TOP_K` and `MIN_SCORE`, and test with representative documents.

## 11. Production checklist

- Self-host n8n if privacy is required.
- Put API, Qdrant and Ollama on a private network.
- Enable API authentication.
- Add TLS/reverse proxy.
- Use backups for Qdrant storage.
- Restrict upload size and allowed formats.
- Add monitoring and log rotation.
- Validate model quality against real company documents.
- Do not treat model output as authoritative without appropriate human review.

## 12. Important

This repository is a production-minded local RAG baseline. It is intentionally transparent and API-first, but no software can honestly guarantee zero bugs on every machine, model version, document format or n8n version. Always run the included smoke tests and validate the exact deployment environment before client production use.

License: MIT.
