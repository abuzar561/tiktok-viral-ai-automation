# Setup Guide

This guide walks through running the local scraper API and connecting it to the n8n workflow.

## Prerequisites

- Python 3.10 or newer
- Google Chrome
- Node.js 20 or newer for local validation
- n8n Desktop, n8n self-hosted, or another n8n instance that can reach the Flask API
- Ollama running locally

## 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## 2. Configure Environment

The app works with defaults, but you can copy `.env.example` and export values in your shell if needed.

Important defaults:

- API URL: `http://localhost:5000`
- Default hashtag: `funny`
- Default limit: `5`
- Max per request: `20`

## 3. Start Ollama

Install Ollama and pull the model used by the workflow:

```bash
ollama pull llama3.1
```

Keep Ollama running while n8n executes the workflow.

## 4. Start the Scraper API

```bash
python src/tiktok_deep_scrape.py
```

Health check:

```bash
curl http://localhost:5000/health
```

Scrape test:

```bash
curl -X POST http://localhost:5000/scrape \
  -H "Content-Type: application/json" \
  -d "{\"hashtag\":\"funny\",\"limit\":3}"
```

## 5. Import the n8n Workflow

1. Open n8n.
2. Import `workflow/tiktok-viral-ai-automation.json`.
3. Open the `Scrape TikTok Trends` node.
4. Confirm the API URL is correct for your environment.
5. Connect your Ollama credential to the `Ollama Chat Model` node.
6. Run the manual trigger.

## 6. Localhost Notes

If n8n runs on your machine, `http://localhost:5000/scrape` is usually correct.

If n8n runs in Docker, change the workflow URL to:

```text
http://host.docker.internal:5000/scrape
```

If n8n runs in the cloud, your local Flask API will not be reachable unless you expose it through a secure tunnel or deploy the API.
