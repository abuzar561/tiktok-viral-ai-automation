# Workflow Guide

The n8n workflow has five main nodes.

| Node | Purpose |
| --- | --- |
| Manual Test Trigger | Starts the workflow manually |
| Scrape TikTok Trends | Calls the local Flask `/scrape` endpoint |
| Build Trend Prompt | Ranks videos and prepares a structured prompt |
| Generate Viral Script | Sends the prompt to the LLM chain |
| Ollama Chat Model | Provides local AI generation |

## Ranking Logic

The `Build Trend Prompt` node calculates:

```text
likes + comments * 2 + shares * 3 + saves * 2
```

It then divides that score by view count to estimate engagement rate and sends the strongest videos to Ollama.

## AI Output

The prompt asks Ollama to return strict JSON with:

- `trend_summary`
- `winning_pattern`
- `original_hook`
- `video_script`
- `caption`
- `suggested_hashtags`
- `production_notes`

## Template Values

The public workflow uses:

```text
http://localhost:5000/scrape
```

Change this URL if your n8n instance runs somewhere else.

## Credential Setup

The workflow does not include exported credentials. After import, attach your own Ollama credential to the `Ollama Chat Model` node.
