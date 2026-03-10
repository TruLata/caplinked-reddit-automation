"""
Blog Scraper for LinkedIn Automation
Extracts latest blog posts from CapLinked blog for LinkedIn content generation
"""

import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BLOG_URL = "https://www.caplinked.com/blog/"

def scrape_blog_posts(limit=3):
    """
    Scrape latest blog posts from CapLinked blog
    
    Args:
        limit: Number of posts to retrieve (default 3)
    
    Returns:
        List of blog post dictionaries with title, content, and URL
    """
    try:
        logger.info(f"Fetching blog posts from {BLOG_URL}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(BLOG_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find blog post links - adjust selectors based on CapLinked blog structure
        posts = []
        
        # Look for post containers (adjust selector if needed)
        post_containers = soup.find_all('article', limit=limit)
        
        if not post_containers:
            # Alternative selector if articles not found
            post_containers = soup.find_all('div', class_='post', limit=limit)
        
        if not post_containers:
            # Another alternative
            post_containers = soup.find_all('div', class_='blog-post', limit=limit)
        
        for container in post_containers:
            try:
                # Extract title
                title_elem = container.find('h2') or container.find('h3') or container.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                
                # Extract URL
                link_elem = container.find('a', href=True)
                if not link_elem:
                    continue
                
                url = link_elem['href']
                if not url.startswith('http'):
                    url = BLOG_URL.rstrip('/') + url
                
                # Extract excerpt/content
                excerpt_elem = container.find('p') or container.find('div', class_='excerpt')
                excerpt = excerpt_elem.get_text(strip=True) if excerpt_elem else ""
                
                # Limit excerpt to first 300 characters
                if len(excerpt) > 300:
                    excerpt = excerpt[:297] + "..."
                
                posts.append({
                    'title': title,
                    'excerpt': excerpt,
                    'url': url,
                    'scraped_at': datetime.now().isoformat()
                })
                
                logger.info(f"Scraped: {title}")
            
            except Exception as e:
                logger.warning(f"Error scraping post: {e}")
                continue
        
        logger.info(f"Successfully scraped {len(posts)} blog posts")
        return posts
    
    except requests.RequestException as e:
        logger.error(f"Error fetching blog: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in blog scraper: {e}")
        return []


def get_blog_content(url):
    """
    Get full content from a specific blog post
    
    Args:
        url: Blog post URL
    
    Returns:
        Dictionary with full post content
    """
    try:
        logger.info(f"Fetching full content from {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('h1')
        title = title.get_text(strip=True) if title else "Untitled"
        
        # Extract main content
        content_elem = soup.find('article') or soup.find('div', class_='post-content') or soup.find('div', class_='content')
        
        if content_elem:
            # Remove script and style elements
            for script in content_elem(['script', 'style']):
                script.decompose()
            
            content = content_elem.get_text(separator=' ', strip=True)
        else:
            content = ""
        
        # Limit content to first 4000 characters for processing
        if len(content) > 4000:
            content = content[:4000]
        
        return {
            'title': title,
            'content': content,
            'url': url
        }
    
    except Exception as e:
        logger.error(f"Error fetching blog content: {e}")
        return None


if __name__ == "__main__":
    # Test the scraper
    posts = scrape_blog_posts(limit=3)
    
    for i, post in enumerate(posts, 1):
        print(f"\n--- Post {i} ---")
        print(f"Title: {post['title']}")
        print(f"URL: {post['url']}")
        print(f"Excerpt: {post['excerpt'][:100]}...")
