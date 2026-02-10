import praw
import os
import time

REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID" )
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "CapLinked-Bot/1.0")

def authenticate_reddit():
    print("--- Authenticating with Reddit ---")
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        print("ERROR: Reddit credentials not set in environment variables.")
        return None
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        print("Successfully authenticated with Reddit.")
        return reddit
    except Exception as e:
        print(f"ERROR: Failed to authenticate with Reddit. Details: {e}")
        return None

def search_and_post_to_reddit(reddit, query, subreddit_name, post_content):
    print(f"--- Searching Reddit for: {query} ---")
    try:
        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.search(query, time_filter="week", limit=5)
        post_list = list(posts)
        if post_list:
            print(f"Found {len(post_list)} posts in r/{subreddit_name} matching '{query}'")
            for post in post_list:
                print(f"  - {post.title} (Score: {post.score})")
        else:
            print(f"No posts found in r/{subreddit_name} matching '{query}'")
        return post_list
    except Exception as e:
        print(f"ERROR: Failed to search Reddit. Details: {e}")
        return []

def run_reddit_scraper():
    reddit = authenticate_reddit()
    if not reddit:
        print("--- Reddit scraper aborted: Could not authenticate. ---")
        return
    queries = ["virtual data room", "VDR", "M&A", "due diligence"]
    subreddits = ["investing", "finance", "business"]
    for query in queries:
        for subreddit in subreddits:
            search_and_post_to_reddit(reddit, query, subreddit, "")
            time.sleep(2)
    print("--- Reddit scraper finished ---")

if __name__ == "__main__":
    run_reddit_scraper()
