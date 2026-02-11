import requests
from bs4 import BeautifulSoup
import time
import random

REDDIT_SEARCH_URL = "https://www.reddit.com/search"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64 ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
]

def scrape_reddit_posts(query, limit=5):
    print(f"--- Searching Reddit for: {query} ---")
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }
        params = {"q": query, "type": "link"}
        response = requests.get(REDDIT_SEARCH_URL, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("a", {"data-testid": "post-title"}, limit=limit)
        post_list = []
        for post in posts:
            title = post.get_text(strip=True)
            link = post.get("href")
            if title and link:
                if not link.startswith("http" ):
                    link = f"https://www.reddit.com{link}"
                post_list.append({"title": title, "link": link} )
                print(f"  - {title}")
        print(f"Found {len(post_list)} posts")
        return post_list
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to scrape Reddit. Details: {e}")
        return []

def run_reddit_scraper():
    print("--- Starting Reddit Scraper ---")
    queries = ["virtual data room", "VDR", "M&A", "due diligence", "investment banking"]
    all_posts = []
    for query in queries:
        posts = scrape_reddit_posts(query, limit=5)
        all_posts.extend(posts)
        time.sleep(random.uniform(2, 5))
    print(f"--- Reddit scraper finished. Found {len(all_posts)} total posts. ---")
    return all_posts

if __name__ == "__main__":
    run_reddit_scraper()
