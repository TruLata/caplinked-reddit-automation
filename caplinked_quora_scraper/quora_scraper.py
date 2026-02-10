import requests
from bs4 import BeautifulSoup
import time

QUORA_SEARCH_URL = "https://www.quora.com/search"

def scrape_quora_questions(query, limit=5 ):
    print(f"--- Searching Quora for: {query} ---")
    try:
        params = {"q": query}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(QUORA_SEARCH_URL, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        questions = soup.find_all("a", class_="q-box", limit=limit)
        question_list = []
        for question in questions:
            title = question.get_text(strip=True)
            link = question.get("href")
            if title and link:
                if not link.startswith("http" ):
                    link = f"https://www.quora.com{link}"
                question_list.append({"title": title, "link": link} )
                print(f"  - {title}")
        print(f"Found {len(question_list)} questions")
        return question_list
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to scrape Quora. Details: {e}")
        return []

def run_quora_scraper():
    print("--- Starting Quora Scraper ---")
    queries = ["virtual data room", "VDR", "M&A", "due diligence", "investment banking"]
    all_questions = []
    for query in queries:
        questions = scrape_quora_questions(query, limit=5)
        all_questions.extend(questions)
        time.sleep(2)
    print(f"--- Quora scraper finished. Found {len(all_questions)} total questions. ---")
    return all_questions

if __name__ == "__main__":
    run_quora_scraper()
