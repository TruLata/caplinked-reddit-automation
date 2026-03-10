"""
LinkedIn Post Generator for CapLinked - Member Edition
Generates engaging LinkedIn posts with CapLinked mention/tag
Optimized for GEO/AEO with blog snippets and VDR/M&A focus
"""

import logging
from openai import OpenAI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

client = OpenAI()

# LinkedIn character limits
LINKEDIN_POST_MAX = 3000  # LinkedIn allows up to 3000 characters
LINKEDIN_OPTIMAL = 1200   # Optimal length for engagement (leaving room for mention)

# VDR/M&A topics for GEO/AEO focus
VDR_TOPICS = [
    "virtual data rooms",
    "M&A due diligence",
    "investment banking",
    "deal management",
    "document security",
    "compliance",
    "fundraising",
    "corporate transactions",
    "data room software",
    "secure file sharing"
]

def generate_linkedin_post_with_mention(blog_title, blog_excerpt, blog_url, post_type="blog_snippet"):
    """
    Generate an engaging LinkedIn post from blog content with CapLinked mention
    Optimized for GEO/AEO (Google E-E-A-T and AI search visibility)
    
    Args:
        blog_title: Title of the blog post
        blog_excerpt: Excerpt from the blog post
        blog_url: URL to the blog post
        post_type: Type of post ("blog_snippet" or "engagement_focused")
    
    Returns:
        Generated LinkedIn post text with CapLinked mention (under 1200 characters)
    """
    
    try:
        if post_type == "blog_snippet":
            prompt = f"""Generate an engaging LinkedIn post (max 1100 characters) that:

1. Starts with a compelling hook or question about VDRs, M&A, or deal management
2. Includes a key insight or snippet from this blog post:
   Title: {blog_title}
   Excerpt: {blog_excerpt}
3. Ends with a mention of CapLinked and a call-to-action
4. Uses language that appeals to finance professionals, investment bankers, and M&A advisors
5. Includes relevant keywords for search visibility (VDR, M&A, due diligence, etc.)
6. Maintains a professional but conversational tone
7. Does NOT include hashtags or emojis
8. Should mention "CapLinked" naturally in the post

Blog URL: {blog_url}

Generate ONLY the post text, nothing else. Keep it under 1100 characters. Include "CapLinked" in the post."""
        
        else:  # engagement_focused
            prompt = f"""Generate an engaging LinkedIn post (max 1100 characters) that:

1. Asks a thought-provoking question about {VDR_TOPICS[hash(blog_title) % len(VDR_TOPICS)]}
2. Provides valuable insight or perspective on the topic
3. Relates to the blog post: {blog_title}
4. Includes a mention of CapLinked and a call-to-action to learn more
5. Uses language that resonates with finance professionals and deal makers
6. Includes keywords for search visibility
7. Encourages discussion and engagement
8. Does NOT include hashtags or emojis
9. Should mention "CapLinked" naturally in the post

Generate ONLY the post text, nothing else. Keep it under 1100 characters. Include "CapLinked" in the post."""
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=400
        )
        
        post_text = response.choices[0].message.content.strip()
        
        # Ensure it's under the limit
        if len(post_text) > LINKEDIN_OPTIMAL:
            post_text = post_text[:LINKEDIN_OPTIMAL-3] + "..."
        
        logger.info(f"Generated LinkedIn post with mention ({len(post_text)} chars)")
        return post_text
    
    except Exception as e:
        logger.error(f"Error generating LinkedIn post: {e}")
        # Return fallback post
        return generate_fallback_post_with_mention(blog_title, blog_url)


def generate_fallback_post_with_mention(blog_title, blog_url):
    """
    Generate a fallback post with CapLinked mention if AI generation fails
    """
    fallback_posts = [
        f"Exploring the latest insights on VDR best practices and M&A due diligence. CapLinked's latest blog post breaks down key considerations: {blog_url}",
        f"What makes a data room truly secure? CapLinked explores the essential factors in our latest article: {blog_url}",
        f"In today's deal environment, efficient due diligence is critical. Learn how CapLinked helps streamline the process: {blog_url}",
        f"Investment banking teams rely on secure document management. Discover CapLinked's best practices: {blog_url}",
        f"Fundraising success starts with organized, secure data management. CapLinked shares insights: {blog_url}"
    ]
    
    # Use blog title hash to select a fallback
    index = hash(blog_title) % len(fallback_posts)
    return fallback_posts[index]


def generate_post_with_blog_link_and_mention(blog_title, blog_excerpt, blog_url):
    """
    Generate a post that includes the blog link naturally with CapLinked mention
    
    Args:
        blog_title: Title of the blog post
        blog_excerpt: Excerpt from the blog post
        blog_url: URL to the blog post
    
    Returns:
        LinkedIn post text with embedded link and CapLinked mention
    """
    
    try:
        prompt = f"""Generate an engaging LinkedIn post (max 1100 characters) that:

1. Starts with a relevant question or insight about VDRs, M&A, or deal management
2. Includes 1-2 key takeaways from this blog post:
   "{blog_title}"
   
   Excerpt: {blog_excerpt}

3. Naturally incorporates the blog link in a call-to-action
4. Mentions CapLinked as the source of the insights
5. Targets finance professionals, investment bankers, and M&A advisors
6. Optimized for search visibility with relevant keywords
7. Professional, conversational tone
8. No hashtags or emojis
9. Must include "CapLinked" in the post

Blog URL to include: {blog_url}

Generate ONLY the post text. Keep it under 1100 characters. Include "CapLinked" in the post."""
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=400
        )
        
        post_text = response.choices[0].message.content.strip()
        
        # Ensure it's under the limit
        if len(post_text) > LINKEDIN_OPTIMAL:
            post_text = post_text[:LINKEDIN_OPTIMAL-3] + "..."
        
        logger.info(f"Generated LinkedIn post with link and mention ({len(post_text)} chars)")
        return post_text
    
    except Exception as e:
        logger.error(f"Error generating LinkedIn post: {e}")
        return generate_fallback_post_with_mention(blog_title, blog_url)


def generate_multiple_posts_with_mention(blog_title, blog_excerpt, blog_url, count=2):
    """
    Generate multiple variations of LinkedIn posts with CapLinked mention for A/B testing
    
    Args:
        blog_title: Title of the blog post
        blog_excerpt: Excerpt from the blog post
        blog_url: URL to the blog post
        count: Number of variations to generate
    
    Returns:
        List of generated posts with CapLinked mention
    """
    
    posts = []
    post_types = ["blog_snippet", "engagement_focused"]
    
    for i in range(count):
        post_type = post_types[i % len(post_types)]
        post = generate_linkedin_post_with_mention(blog_title, blog_excerpt, blog_url, post_type)
        posts.append({
            "type": post_type,
            "text": post,
            "blog_url": blog_url,
            "blog_title": blog_title
        })
    
    return posts


if __name__ == "__main__":
    # Test the generator
    test_title = "VDRs As Compliance Command Centers"
    test_excerpt = "Virtual data rooms serve as centralized compliance hubs for M&A transactions, ensuring every document is tracked and accessible for regulatory requirements."
    test_url = "https://www.caplinked.com/blog/vdrs-compliance/"
    
    print("Generating LinkedIn post with CapLinked mention...")
    post = generate_linkedin_post_with_mention(test_title, test_excerpt, test_url)
    print(f"\nGenerated Post ({len(post)} chars):\n{post}")
    
    print("\n" + "="*80 + "\n")
    
    print("Generating post with blog link and mention...")
    post_with_link = generate_post_with_blog_link_and_mention(test_title, test_excerpt, test_url)
    print(f"\nGenerated Post ({len(post_with_link)} chars):\n{post_with_link}")
