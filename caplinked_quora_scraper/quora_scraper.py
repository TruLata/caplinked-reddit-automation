'''
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

# Configuration
QUORA_TOPICS = [
    "virtual-data-rooms-VDR",
    "Mergers-and-Acquisitions-M-A",
    "Due-Diligence",
    "Investment-Banking",
    "Venture-Capital",
    "Startups"
]

BASE_URL = "https://www.quora.com/topic/"

def scrape_quora():
    results = []
    print("--- Initializing Quora Scraper ---")
    for topic in QUORA_TOPICS:
        url = f"{BASE_URL}{topic}/all_questions"
        print(f"  -> Scraping topic: {topic}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        }
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # This selector is fragile and may break if Quora changes their HTML structure.
            question_elements = soup.select('a[href*="/question/"]')

            for element in question_elements:
                question_text_span = element.find("span", class_="qu-bold")
                if question_text_span:
                    question_text = question_text_span.get_text(strip=True)
                    question_url = element.get('href')
                    if question_url and not question_url.startswith("http"):
                        question_url = f"https://www.quora.com{question_url}"

                    # Avoid duplicates
                    if not any(d['link'] == question_url for d in results):
                        print(f"    [Question Found] {question_text}")
                        results.append({
                            "topic": topic,
                            "question": question_text,
                            "link": question_url,
                            "timestamp": datetime.now().isoformat()
                        })

        except requests.exceptions.RequestException as e:
            print(f"    ERROR: Could not scrape topic {topic}. Details: {e}")
        
        time.sleep(3) # Be respectful of Quora's servers

    print(f"--- Quora scraping session finished. Found {len(results)} unique questions. ---
")
    return results

if __name__ == "__main__":
    scraped_data = scrape_quora()
    if scraped_data:
        print(f"Successfully scraped {len(scraped_data)} questions from Quora.")
    else:
        print("No new relevant questions found in this session.")
'''
