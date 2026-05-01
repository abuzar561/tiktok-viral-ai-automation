# Contributing

Thanks for improving this project.

## Useful Contributions

- Improve scraper stability.
- Add provider-specific setup notes for n8n and Ollama.
- Improve trend ranking logic.
- Add tests around prompt preparation and API validation.
- Document real troubleshooting cases.

## Development Workflow

1. Create a branch from `main`.
2. Make your changes.
3. Run:

```bash
node scripts/validate-project.js
python -m py_compile src/tiktok_deep_scrape.py
```

4. Test the Flask API locally.
5. Open a pull request with what changed, why it changed, and how it was tested.

## Security Rules

Do not commit private n8n credential exports, browser profiles, session cookies, generated private data, or API tokens.
