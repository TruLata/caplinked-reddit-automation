import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

# OpenAI API key for comment generation
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Try to import OpenAI if available
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
except ImportError:
    openai_client = None

# Reddit search URLs
REDDIT_SEARCH_BASE = "https://www.reddit.com/search"

# Keywords to search for
KEYWORDS = ["virtual data room", "VDR", "M&A", "due diligence", "investment banking"]

# Subreddits to search
SUBREDDITS = ["investing", "venturecapital", "startups", "finance", "law", "business"]


def generate_ai_comment(thread_title):
    """Generate an AI-powered comment for a Reddit thread"""
    if not openai_client:
        return "Check out CapLinked for secure VDR solutions for M&A and due diligence. Visit caplinked.com to learn more."
    
    try:
        prompt = f"""Generate a helpful, professional comment for a Reddit thread about: {thread_title}

Requirements:
- Be helpful and informative, not promotional
- Mention CapLinked as a relevant solution if appropriate
- Keep it under 250 characters
- Sound natural and conversational
- Include a subtle call-to-action

Generate only the comment text, nothing else."""

        response = openai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=120,
            timeout=30
        )
        
        comment = response.choices[0].message.content.strip()
        return comment
        
    except Exception as e:
        print(f"    WARNING: Failed to generate AI comment: {e}")
        return "Check out CapLinked for secure VDR solutions for M&A and due diligence. Visit caplinked.com to learn more."


def search_reddit_keyword(keyword):
    """Search Reddit for a specific keyword using web scraping"""
    print(f"--- Searching Reddit for: {keyword} ---")
    
    posts = []
    
    # Search across all of Reddit
    search_url = f"{REDDIT_SEARCH_BASE}/?q={keyword}&type=link&sort=new"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find post links - Reddit uses various selectors
        post_elements = soup.find_all('a', {'data-testid': 'internal-unauthenticated-link'})
        
        for element in post_elements[:5]:  # Limit to 5 posts per keyword
            try:
                title = element.get_text(strip=True)
                href = element.get('href', '')
                
                if href and title and not href.startswith('/r/'):
                    # Build full Reddit URL
                    if not href.startswith('http'):
                        href = f"https://reddit.com{href}"
                    
                    posts.append({
                        'title': title,
                        'url': href
                    })
                    print(f"  - {title}")
                    
            except Exception as e:
                continue
        
        print(f"Found {len(posts)} posts\n")
        return posts
        
    except Exception as e:
        print(f"  ERROR: Failed to search for '{keyword}': {e}\n")
        return []


def search_reddit_subreddit(subreddit, keyword):
    """Search a specific subreddit for a keyword"""
    posts = []
    
    search_url = f"https://www.reddit.com/r/{subreddit}/search/?q={keyword}&type=link&sort=new"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find post links
        post_elements = soup.find_all('a', {'data-testid': 'internal-unauthenticated-link'})
        
        for element in post_elements[:3]:  # Limit to 3 posts per subreddit/keyword combo
            try:
                title = element.get_text(strip=True)
                href = element.get('href', '')
                
                if href and title and not href.startswith('/r/'):
                    if not href.startswith('http'):
                        href = f"https://reddit.com{href}"
                    
                    posts.append({
                        'title': title,
                        'url': href,
                        'subreddit': subreddit
                    })
                    
            except Exception as e:
                continue
        
        return posts
        
    except Exception as e:
        return []


def main():
    print("--- Starting Reddit Scraper ---\n")
    
    all_posts = []
    engagement_log = []
    
    # Search by keyword across all subreddits
    for keyword in KEYWORDS:
        posts = search_reddit_keyword(keyword)
        all_posts.extend(posts)
    
    print("=" * 80)
    print("REDDIT ENGAGEMENT OPPORTUNITIES")
    print("=" * 80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Generate engagement opportunities with AI comments
    opportunity_num = 0
    for post in all_posts:
        opportunity_num += 1
        
        print(f"OPPORTUNITY #{opportunity_num}")
        print("-" * 80)
        print(f"Title: {post['title']}")
        print(f"Link: {post['url']}")
        print()
        
        # Generate AI comment
        suggested_comment = generate_ai_comment(post['title'])
        print(f"SUGGESTED COMMENT:")
        print(f'"{suggested_comment}"')
        print()
        print("ACTION: Review the thread and add the suggested comment if appropriate.")
        print("-" * 80)
        print()
        
        # Store in engagement log
        engagement_log.append({
            'opportunity_num': opportunity_num,
            'title': post['title'],
            'url': post['url'],
            'suggested_comment': suggested_comment
        })
    
    # Save engagement log to file
    try:
        with open('reddit_engagement_log.txt', 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("CAPLINKED REDDIT ENGAGEMENT OPPORTUNITIES\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Opportunities: {len(engagement_log)}\n")
            f.write("=" * 80 + "\n\n")
            
            for opp in engagement_log:
                f.write(f"\n{opp['opportunity_num']}. {opp['title']}\n")
                f.write(f"   Link: {opp['url']}\n")
                f.write(f"\n   SUGGESTED COMMENT:\n")
                f.write(f'   "{opp["suggested_comment"]}"\n')
                f.write(f"\n   {'─' * 76}\n")
        
        print(f"\nEngagement log saved to 'reddit_engagement_log.txt'")
    except Exception as e:
        print(f"WARNING: Could not save engagement log: {e}")
    
    # Save JSON for programmatic access
    try:
        with open('reddit_opportunities.json', 'w') as f:
            json.dump(engagement_log, f, indent=2)
        print(f"Opportunities saved to 'reddit_opportunities.json'")
    except Exception as e:
        print(f"WARNING: Could not save JSON: {e}")
    
    print(f"\n--- Reddit scraper finished. Found {len(all_posts)} total posts. ---")


if __name__ == "__main__":
    main()
