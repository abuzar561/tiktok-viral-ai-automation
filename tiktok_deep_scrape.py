import time
import json
import random
import re
import os 
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

# ==========================================
# FLASK APP SETUP
# ==========================================
app = Flask(__name__)

# ==========================================
# CONFIGURATION
# ==========================================
HEADLESS_MODE = True  # API ke liye Headless True rakha hai taaki background me chale
# TARGET_HASHTAG aur TARGET_SAVED_VIDEOS ab n8n se aayenge

def extract_hashtags(description):
    if not description: return []
    return re.findall(r"#\w+", description)

def get_video_details_and_time(driver, video_url):
    try:
        driver.get(video_url)
        time.sleep(random.uniform(2, 4)) # Time thoda kam kiya hai for faster API response
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Helper to find values using Regex pattern
        def extract_val(key):
            match = re.search(f'"{key}"\s*:\s*"?(\d+)"?', page_source)
            return int(match.group(1)) if match else 0

        # Extract stats
        likes = extract_val("diggCount")
        views = extract_val("playCount")
        comments = extract_val("commentCount")
        shares = extract_val("shareCount")
        saves = extract_val("collectCount")

        # Description & Author
        desc_elem = soup.find(attrs={"data-e2e": "browse-video-desc"})
        description = desc_elem.text.strip() if desc_elem else ""
        hashtags = extract_hashtags(description)

        author_elem = soup.find(attrs={"data-e2e": "browse-username"})
        author = author_elem.text.strip() if author_elem else "Unknown"
        
        return {
            "author": author,
            "likes": likes,         
            "comments": comments,   
            "shares": shares,       
            "videoCount": views,    
            "collectCount": saves,  
            "description": description,
            "hashtags": hashtags
        }

    except Exception as e:
        print(f"Error scraping details: {e}")
        return None

# Main scraping logic ko function banaya jo parameters accept kare
def scrape_tiktok_data(target_hashtag, max_videos):
    options = Options()
    if HEADLESS_MODE: options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    all_scraped_data = [] 
    candidates = [] 

    try:
        # --- STEP 1: SEARCH PAGE ---
        url = f"https://www.tiktok.com/tag/{target_hashtag}"
        driver.get(url)
        time.sleep(3)

        # Thoda scroll karenge
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        all_anchors = soup.find_all('a', href=True)
        
        for a in all_anchors:
            href = a['href']
            if "/video/" in href:
                if any(c['link'] == href for c in candidates): continue
                candidates.append({"link": href})

        # --- STEP 2: OPEN VIDEO & SCRAPE ---
        saved_count_session = 0
        
        for index, item in enumerate(candidates):
            if saved_count_session >= max_videos:
                break

            link = item['link']
            details = get_video_details_and_time(driver, link)
            
            if details:
                record = {
                    "hashtag_searched": target_hashtag,
                    "author": details['author'],
                    "video_link": link,
                    "playCount": details['videoCount'],
                    "diggCount": details['likes'],
                    "commentCount": details['comments'],
                    "shareCount": details['shares'],
                    "collectCount": details['collectCount'],
                    "hashtags": details['hashtags'],
                    "description_full": details['description']
                }
                
                all_scraped_data.append(record)
                saved_count_session += 1
            
            # Thoda wait taaki block na ho, lekin API timeout se bachne ke liye kam rakha hai
            time.sleep(random.uniform(1, 3))

    except Exception as e:
        print(f"Global Error: {e}")
        return {"error": str(e)}

    finally:
        driver.quit()
    
    # Yaha hum directly list return kar rahe hain, file save nahi kar rahe
    return all_scraped_data

# ==========================================
# API ROUTE FOR N8N
# ==========================================
@app.route('/scrape', methods=['POST'])
def run_scraper():
    # n8n se JSON data receive karna
    content = request.json
    
    # Default values agar n8n kuch na bheje
    hashtag = content.get('hashtag', 'funny')
    limit = content.get('limit', 5) # Default 5 videos

    print(f"API Request Received: Hashtag={hashtag}, Limit={limit}")

    # Scraping function call karna
    data = scrape_tiktok_data(hashtag, int(limit))

    # Data ko JSON format mein return karna
    return jsonify(data)

if __name__ == "__main__":
    # Server start on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)