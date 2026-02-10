'''
import praw
import os

# Reddit API credentials will be read from Render's environment variables
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "VDR-Marketing-Bot/0.1 by RevolutionaryCar1356")

# Subreddits to monitor
SUBREDDITS = ["investing", "venturecapital", "startups", "finance", "law", "business"]

# Keywords to search for
KEYWORDS = ["virtual data room", "vdr", "mergers and acquisitions", "due diligence", "caplinked"]

def main():
    print("Initializing Reddit scraper...")
    
    # Check for credentials
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        print("ERROR: Reddit API credentials (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET) not found in environment variables.")
        print("This script cannot run until the Reddit API application is approved and credentials are set in the Render service environment.")
        return

    print("Connecting to Reddit...")
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )
        # Test connection
        print(f"Successfully connected to Reddit as: {reddit.user.me()}")
    except Exception as e:
        print(f"ERROR: Failed to connect to Reddit. Please check your credentials. Details: {e}")
        return

    for subreddit_name in SUBREDDITS:
        print(f"--- Searching subreddit: r/{subreddit_name} ---")
        subreddit = reddit.subreddit(subreddit_name)
        for keyword in KEYWORDS:
            print(f"  -> Searching for keyword: '{keyword}'")
            try:
                # Search for new posts
                for submission in subreddit.search(keyword, sort="new", time_filter="week"):
                    print(f"    [Post Found] Title: {submission.title}")
                    print(f"      URL: {submission.url}")
            except Exception as e:
                print(f"    ERROR: An error occurred while searching r/{subreddit_name} for '{keyword}'. Details: {e}")

    print("--- Reddit scraping session finished. ---")

if __name__ == "__main__":
    main()
'''
