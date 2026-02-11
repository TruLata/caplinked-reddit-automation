import praw
import os
import logging
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reddit_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Reddit API credentials will be read from Render's environment variables
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "VDR-Marketing-Bot/0.1 by RevolutionaryCar1356")

# OpenAI API key for comment generation
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Subreddits to monitor
SUBREDDITS = ["investing", "venturecapital", "startups", "finance", "law", "business"]

# Keywords to search for
KEYWORDS = ["virtual data room", "vdr", "mergers and acquisitions", "due diligence", "caplinked"]

# Initialize OpenAI client if API key is available
openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    logger.warning("OPENAI_API_KEY not set. AI comment generation disabled.")


def generate_ai_comment(thread_title, thread_content=""):
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
- Include a subtle call-to-action (e.g., "Learn more at caplinked.com" or "Check out CapLinked's blog")

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
        logger.warning(f"Failed to generate AI comment: {e}")
        return "Check out CapLinked for secure VDR solutions for M&A and due diligence. Visit caplinked.com to learn more."


def main():
    logger.info("Initializing Reddit scraper...")
    
    # Check for credentials
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        logger.error("ERROR: Reddit API credentials (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET) not found in environment variables.")
        logger.error("This script cannot run until the Reddit API application is approved and credentials are set in the Render service environment.")
        return

    logger.info("Connecting to Reddit...")
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )
        # Test connection
        logger.info(f"Successfully connected to Reddit as: {reddit.user.me()}")
    except Exception as e:
        logger.error(f"ERROR: Failed to connect to Reddit. Please check your credentials. Details: {e}")
        return

    logger.info("=" * 80)
    logger.info("REDDIT ENGAGEMENT OPPORTUNITIES")
    logger.info("=" * 80)
    
    opportunities_found = 0

    for subreddit_name in SUBREDDITS:
        logger.info(f"\n--- Searching subreddit: r/{subreddit_name} ---")
        subreddit = reddit.subreddit(subreddit_name)
        for keyword in KEYWORDS:
            logger.info(f"  -> Searching for keyword: '{keyword}'")
            try:
                # Search for new posts
                for submission in subreddit.search(keyword, sort="new", time_filter="week"):
                    opportunities_found += 1
                    
                    # Build full Reddit URL
                    reddit_url = f"https://reddit.com{submission.permalink}"
                    
                    logger.info("")
                    logger.info("-" * 80)
                    logger.info(f"OPPORTUNITY #{opportunities_found}")
                    logger.info("-" * 80)
                    logger.info(f"Title: {submission.title}")
                    logger.info(f"Subreddit: r/{subreddit_name}")
                    logger.info(f"Author: u/{submission.author}")
                    logger.info(f"Score: {submission.score}")
                    logger.info(f"Comments: {submission.num_comments}")
                    logger.info("")
                    logger.info(f"THREAD LINK: {reddit_url}")
                    logger.info("")
                    
                    # Generate and log AI comment
                    suggested_comment = generate_ai_comment(submission.title, submission.selftext[:300])
                    logger.info(f"SUGGESTED COMMENT:")
                    logger.info(f'"{suggested_comment}"')
                    logger.info("")
                    logger.info("ACTION: Review the thread and add the suggested comment if appropriate.")
                    logger.info("-" * 80)
                    
            except Exception as e:
                logger.error(f"    ERROR: An error occurred while searching r/{subreddit_name} for '{keyword}'. Details: {e}")

    logger.info("")
    logger.info("=" * 80)
    logger.info(f"Reddit scraping session finished. Found {opportunities_found} engagement opportunities.")
    logger.info("Check the log above for thread links and suggested comments.")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
