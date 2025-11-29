# tiktok-viral-ai-automation
# 🚀 TikTok Viral Content Automation (Python + n8n + Ollama)

An autonomous agent that scrapes trending TikTok videos, analyzes engagement metrics, and uses Local AI (Ollama) to generate viral video scripts, hooks, and captions.

## 🏗 Architecture

**Python (Selenium/Flask)** --> **n8n (Workflow Engine)** --> **Ollama (Llama3 AI)**

1.  **Scraper:** A Python script runs a headless Chrome browser to scrape video stats (Views, Likes, Description, Hashtags).
2.  **API:** Exposed via Flask so n8n can trigger the scrape via HTTP Request.
3.  **Logic:** n8n calculates the "Engagement Rate" and picks the winning video.
4.  **GenAI:** Ollama (hosted locally) receives the context and hallucinates/invents a new creative scenario + script based on the winning trend.

## ✨ Features

* **⚡ Supercharged Scraping:** Optimized Selenium settings (Eager loading, Image blocking) for fast data extraction.
* **🔌 API-First Design:** No local JSON files; data streams directly to the workflow via Flask.
* **🤖 Local AI Integration:** Uses Ollama (Llama3) for privacy-focused, free AI generation.
* **🛡️ Smart Filtering:** Automatically removes "Unknown" authors or ads to prevent AI hallucination on bad data.
* **📝 JSON Output:** AI is prompt-engineered to return strict JSON for downstream automation.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Browser Automation:** Selenium & WebDriver Manager
* **API Framework:** Flask
* **Workflow Automation:** n8n (Self-hosted or Desktop)
* **AI Model:** Ollama (running Llama3 or Mistral)

## 🚀 Setup & Usage

### 1. Clone the Repo
```bash
git clone [https://github.com/YOUR_USERNAME/tiktok-viral-ai-automation.git](https://github.com/YOUR_USERNAME/tiktok-viral-ai-automation.git)
cd tiktok-viral-ai-automation

pip install -r requirements.txt

{
  "hashtag": "funny",
  "limit": 5
}
