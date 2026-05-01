# Troubleshooting

## Python Is Not Found

Install Python 3.10 or newer and ensure it is available on your PATH.

On Windows, try:

```powershell
py -3 --version
```

## ChromeDriver Fails

`webdriver-manager` downloads the matching ChromeDriver version. If this fails:

- Confirm Google Chrome is installed.
- Confirm the machine can access the internet.
- Delete any stale cached driver and rerun the script.

## TikTok Returns No Videos

Possible causes:

- TikTok blocked the automated browser.
- The hashtag has little public content.
- The page structure changed.
- A cookie or region prompt blocked the page.

Try a different hashtag, reduce the request frequency, or run with `HEADLESS_MODE=false` to inspect the browser.

## n8n Cannot Reach the API

Check where n8n is running:

- Local machine: use `http://localhost:5000/scrape`.
- Docker: use `http://host.docker.internal:5000/scrape`.
- Cloud: deploy the API or use a secure tunnel.

## Ollama Node Fails

Possible causes:

- Ollama is not running.
- The selected model is not pulled.
- The n8n Ollama credential points to the wrong base URL.

Run:

```bash
ollama pull llama3.1
```

Then test the model directly before rerunning the workflow.

## AI Output Is Not Valid JSON

Local models can occasionally ignore formatting instructions. Re-run the workflow or use a stronger model in the Ollama node.

## Scraping Is Slow

Reduce `limit` or `SCROLL_PASSES`, but keep request delays conservative to avoid triggering blocks.
