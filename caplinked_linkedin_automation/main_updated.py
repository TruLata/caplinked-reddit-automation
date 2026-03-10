"""
CapLinked LinkedIn Automation - Main Orchestration Script (Updated with Images)
Runs the complete pipeline: scrape blog -> generate posts -> generate images -> post to LinkedIn
"""

import logging
import json
import os
from datetime import datetime
from blog_scraper import scrape_blog_posts, get_blog_content
from linkedin_post_generator import generate_post_with_blog_link
from linkedin_poster_updated import LinkedInPoster, get_linkedin_credentials
from image_generator import LinkedInImageGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_linkedin_automation():
    """
    Main automation pipeline with image generation
    """
    
    logger.info("="*80)
    logger.info("Starting CapLinked LinkedIn Automation (with Image Generation)")
    logger.info("="*80)
    
    # Get LinkedIn credentials
    access_token, org_id = get_linkedin_credentials()
    
    if not access_token or not org_id:
        logger.error("Cannot proceed without LinkedIn credentials")
        return False
    
    # Initialize LinkedIn poster
    poster = LinkedInPoster(access_token, org_id)
    
    # Initialize image generator
    image_generator = LinkedInImageGenerator()
    
    # Scrape blog posts
    logger.info("Step 1: Scraping blog posts...")
    blog_posts = scrape_blog_posts(limit=2)  # Get 2 posts per day
    
    if not blog_posts:
        logger.warning("No blog posts found")
        return False
    
    logger.info(f"Found {len(blog_posts)} blog posts")
    
    # Track posted content
    posted_content = []
    
    # Process each blog post
    for i, post in enumerate(blog_posts, 1):
        try:
            logger.info(f"\nProcessing post {i}/{len(blog_posts)}: {post['title']}")
            
            # Get full blog content
            blog_content = get_blog_content(post['url'])
            
            if not blog_content:
                logger.warning(f"Could not fetch full content for {post['title']}")
                continue
            
            # Generate LinkedIn post
            logger.info("Step 2: Generating LinkedIn post...")
            linkedin_post = generate_post_with_blog_link(
                blog_title=post['title'],
                blog_excerpt=post['excerpt'],
                blog_url=post['url']
            )
            
            if not linkedin_post:
                logger.warning(f"Failed to generate post for {post['title']}")
                continue
            
            logger.info(f"Generated post ({len(linkedin_post)} chars):\n{linkedin_post}\n")
            
            # Skip image generation for now - Runway API issues
            logger.info("Step 3: Skipping image generation (Runway API issues)")
            image_url = None
            
            # Post to LinkedIn
            logger.info("Step 4: Posting to LinkedIn...")
            post_id = poster.post_blog_content_with_image(
                blog_title=post['title'],
                post_text=linkedin_post,
                blog_url=post['url'],
                image_url=image_url
            )
            
            if post_id:
                posted_content.append({
                    "blog_title": post['title'],
                    "blog_url": post['url'],
                    "linkedin_post": linkedin_post,
                    "image_url": image_url,
                    "post_id": post_id,
                    "timestamp": datetime.now().isoformat(),
                    "status": "SUCCESS"
                })
                logger.info(f"Successfully posted to LinkedIn: {post_id}")
            else:
                posted_content.append({
                    "blog_title": post['title'],
                    "blog_url": post['url'],
                    "linkedin_post": linkedin_post,
                    "image_url": image_url,
                    "timestamp": datetime.now().isoformat(),
                    "status": "FAILED"
                })
                logger.error(f"Failed to post {post['title']} to LinkedIn")
        
        except Exception as e:
            logger.error(f"Error processing post {i}: {e}")
            continue
    
    # Save results
    logger.info("\nStep 5: Saving results...")
    save_results(posted_content)
    
    logger.info("="*80)
    logger.info("LinkedIn Automation Complete")
    logger.info(f"Posted {len([p for p in posted_content if p['status'] == 'SUCCESS'])} posts")
    logger.info("="*80)
    
    return True


def save_results(posted_content):
    """
    Save posting results to files
    
    Args:
        posted_content: List of posted content records
    """
    
    try:
        # Save as JSON
        with open('linkedin_posts.json', 'w') as f:
            json.dump(posted_content, f, indent=2)
        logger.info("Saved results to linkedin_posts.json")
        
        # Save as human-readable log
        with open('linkedin_posting_log.txt', 'a') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Posting Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*80}\n\n")
            
            for item in posted_content:
                f.write(f"Blog Title: {item['blog_title']}\n")
                f.write(f"Blog URL: {item['blog_url']}\n")
                f.write(f"Status: {item['status']}\n")
                if item['status'] == 'SUCCESS':
                    f.write(f"Post ID: {item.get('post_id', 'N/A')}\n")
                if item.get('image_url'):
                    f.write(f"Image URL: {item['image_url']}\n")
                f.write(f"\nLinkedIn Post:\n{item['linkedin_post']}\n")
                f.write(f"\n{'-'*80}\n\n")
        
        logger.info("Saved results to linkedin_posting_log.txt")
    
    except Exception as e:
        logger.error(f"Error saving results: {e}")


if __name__ == "__main__":
    try:
        success = run_linkedin_automation()
        exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)
