import logging
import os
import random
import re
import time
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


app = Flask(__name__)

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

DEFAULT_HASHTAG = os.getenv("DEFAULT_HASHTAG", "funny")
DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "5"))
MAX_LIMIT = int(os.getenv("MAX_LIMIT", "20"))
SCROLL_PASSES = int(os.getenv("SCROLL_PASSES", "3"))
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true").lower() not in {"0", "false", "no"}
REQUEST_DELAY_MIN = float(os.getenv("REQUEST_DELAY_MIN", "1"))
REQUEST_DELAY_MAX = float(os.getenv("REQUEST_DELAY_MAX", "3"))
USER_AGENT = os.getenv(
    "USER_AGENT",
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
)


def extract_hashtags(description: str) -> list[str]:
    if not description:
        return []
    return re.findall(r"#\w+", description)


def parse_stat(page_source: str, key: str) -> int:
    match = re.search(rf'"{re.escape(key)}"\s*:\s*"?(\d+)"?', page_source)
    return int(match.group(1)) if match else 0


def normalize_hashtag(value: str) -> str:
    hashtag = re.sub(r"[^\w]", "", value.replace("#", "").strip())
    if not hashtag:
        raise ValueError("hashtag must contain at least one letter or number")
    return hashtag


def normalize_video_url(href: str) -> str:
    if href.startswith("//"):
        return f"https:{href}"
    return urljoin("https://www.tiktok.com", href)


def create_driver() -> webdriver.Chrome:
    options = Options()

    if HEADLESS_MODE:
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={USER_AGENT}")
    options.page_load_strategy = "eager"

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def get_video_details(driver: webdriver.Chrome, video_url: str) -> dict[str, Any] | None:
    try:
        driver.get(video_url)
        time.sleep(random.uniform(2, 4))

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        description_element = soup.find(attrs={"data-e2e": "browse-video-desc"})
        author_element = soup.find(attrs={"data-e2e": "browse-username"})
        description = description_element.text.strip() if description_element else ""

        return {
            "author": author_element.text.strip() if author_element else "Unknown",
            "video_link": video_url,
            "playCount": parse_stat(page_source, "playCount"),
            "diggCount": parse_stat(page_source, "diggCount"),
            "commentCount": parse_stat(page_source, "commentCount"),
            "shareCount": parse_stat(page_source, "shareCount"),
            "collectCount": parse_stat(page_source, "collectCount"),
            "hashtags": extract_hashtags(description),
            "description_full": description,
        }
    except Exception as error:
        logger.warning("Failed to scrape video details for %s: %s", video_url, error)
        return None


def collect_video_links(driver: webdriver.Chrome, hashtag: str) -> list[str]:
    driver.get(f"https://www.tiktok.com/tag/{hashtag}")
    time.sleep(3)

    for _ in range(SCROLL_PASSES):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    links: list[str] = []
    seen: set[str] = set()

    for anchor in soup.find_all("a", href=True):
        href = normalize_video_url(anchor["href"])
        if "/video/" in href and href not in seen:
            links.append(href)
            seen.add(href)

    return links


def scrape_tiktok_data(target_hashtag: str, max_videos: int) -> list[dict[str, Any]]:
    hashtag = normalize_hashtag(target_hashtag)
    limit = max(1, min(int(max_videos), MAX_LIMIT))
    driver = create_driver()
    results: list[dict[str, Any]] = []

    try:
        candidates = collect_video_links(driver, hashtag)
        logger.info("Found %s candidate videos for #%s", len(candidates), hashtag)

        for video_url in candidates:
            if len(results) >= limit:
                break

            details = get_video_details(driver, video_url)
            if details:
                details["hashtag_searched"] = hashtag
                results.append(details)

            time.sleep(random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX))

        return results
    finally:
        driver.quit()


@app.get("/health")
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@app.post("/scrape")
def run_scraper():
    payload = request.get_json(silent=True) or {}

    try:
        hashtag = normalize_hashtag(str(payload.get("hashtag", DEFAULT_HASHTAG)))
        limit = int(payload.get("limit", DEFAULT_LIMIT))
    except (TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

    logger.info("Scrape request received: hashtag=%s limit=%s", hashtag, limit)

    try:
        data = scrape_tiktok_data(hashtag, limit)
        return jsonify(data)
    except Exception as error:
        logger.exception("Scrape request failed")
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"},
    )
