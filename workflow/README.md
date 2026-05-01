# Workflow Import

Import `tiktok-viral-ai-automation.json` into n8n.

## Required Local Services

- Flask scraper API at `http://localhost:5000/scrape`
- Ollama running with `llama3.1` or another configured local model

## After Import

1. Open `Scrape TikTok Trends`.
2. Confirm the Flask API URL matches your environment.
3. Open `Ollama Chat Model`.
4. Attach your Ollama credential.
5. Run the manual trigger.

The workflow is exported as a public template and intentionally does not include private credentials.
