"""
LinkedIn API Integration for CapLinked - Updated with Image Support
Posts generated content to CapLinked company page automatically with images
"""

import requests
import json
import logging
import os
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# LinkedIn API Configuration
LINKEDIN_API_BASE = "https://api.linkedin.com/rest"
LINKEDIN_API_VERSION = "202312"

class LinkedInPoster:
    """Handle posting to LinkedIn company page via API"""
    
    def __init__(self, access_token, organization_id):
        """
        Initialize LinkedIn poster
        
        Args:
            access_token: LinkedIn OAuth access token
            organization_id: CapLinked organization ID (numeric ID from LinkedIn)
        """
        self.access_token = access_token
        self.organization_id = organization_id
        self.organization_urn = f"urn:li:organization:{organization_id}"
        
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "LinkedIn-Version": "202312"
        }
        
        logger.info(f"Initialized LinkedIn poster for organization: {self.organization_urn}")
    
    def post_text_only(self, text):
        """
        Post text-only content to company page
        
        Args:
            text: Post content (max 3000 characters)
        
        Returns:
            Response from LinkedIn API with post ID
        """
        
        if len(text) > 3000:
            logger.warning(f"Post text exceeds 3000 characters ({len(text)}), truncating")
            text = text[:2997] + "..."
        
        payload = {
            "author": self.organization_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        return self._make_api_request("POST", "/posts", payload)
    
    def post_with_image(self, text, image_url):
        """
        Post content with an image
        
        Args:
            text: Post commentary
            image_url: URL to the image to include
        
        Returns:
            Response from LinkedIn API with post ID
        """
        
        if len(text) > 3000:
            logger.warning(f"Post text exceeds 3000 characters ({len(text)}), truncating")
            text = text[:2997] + "..."
        
        payload = {
            "author": self.organization_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "type": "IMAGE",
                            "originalUrl": image_url
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        return self._make_api_request("POST", "/posts", payload)
    
    def post_with_link(self, text, link_url, link_title="", link_description=""):
        """
        Post content with a link preview
        
        Args:
            text: Post commentary
            link_url: URL to include
            link_title: Title for the link preview
            link_description: Description for the link preview
        
        Returns:
            Response from LinkedIn API with post ID
        """
        
        if len(text) > 3000:
            logger.warning(f"Post text exceeds 3000 characters ({len(text)}), truncating")
            text = text[:2997] + "..."
        
        payload = {
            "author": self.organization_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "type": "ARTICLE",
                            "originalUrl": link_url,
                            "title": link_title[:100] if link_title else "",
                            "description": link_description[:200] if link_description else ""
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        return self._make_api_request("POST", "/posts", payload)
    
    def _make_api_request(self, method, endpoint, data=None):
        """
        Make authenticated request to LinkedIn API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request payload
        
        Returns:
            Response JSON or None if failed
        """
        
        url = f"{LINKEDIN_API_BASE}{endpoint}"
        
        # Debug: log headers being sent
        logger.info(f"Request headers: {self.headers}")
        
        try:
            if method == "POST":
                response = requests.post(
                    url,
                    headers=self.headers,
                    json=data,
                    timeout=30
                )
            elif method == "GET":
                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=30
                )
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return None
            
            # Log response
            logger.info(f"{method} {endpoint} - Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                result = response.json()
                logger.info(f"Success: {json.dumps(result, indent=2)}")
                return result
            
            elif response.status_code == 429:
                logger.warning("Rate limited by LinkedIn API")
                return None
            
            elif response.status_code == 401:
                logger.error("Unauthorized - Invalid access token")
                return None
            
            elif response.status_code == 403:
                logger.error("Forbidden - May lack required permissions")
                return None
            
            else:
                logger.error(f"API Error {response.status_code}: {response.text}")
                return None
        
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def post_blog_content_with_image(self, blog_title, post_text, blog_url, image_url=None):
        """
        Post blog content with image to LinkedIn
        
        Args:
            blog_title: Title of the blog post
            post_text: Generated post text
            blog_url: URL to the blog post
            image_url: URL to generated image (optional)
        
        Returns:
            Post ID if successful, None otherwise
        """
        
        try:
            if image_url:
                logger.info(f"Posting to LinkedIn with image: {blog_title}")
                result = self.post_with_image(post_text, image_url)
            else:
                logger.info(f"Posting to LinkedIn with link: {blog_title}")
                result = self.post_with_link(
                    text=post_text,
                    link_url=blog_url,
                    link_title=blog_title,
                    link_description="Read the full article on CapLinked blog"
                )
            
            if result and "id" in result:
                post_id = result["id"]
                logger.info(f"Successfully posted to LinkedIn. Post ID: {post_id}")
                return post_id
            else:
                logger.error("Failed to get post ID from response")
                return None
        
        except Exception as e:
            logger.error(f"Error posting blog content: {e}")
            return None
    
    def post_blog_content(self, blog_title, post_text, blog_url):
        """
        Post blog content with link to LinkedIn (backward compatible)
        
        Args:
            blog_title: Title of the blog post
            post_text: Generated post text
            blog_url: URL to the blog post
        
        Returns:
            Post ID if successful, None otherwise
        """
        
        return self.post_blog_content_with_image(blog_title, post_text, blog_url, image_url=None)


def get_linkedin_credentials():
    """
    Get LinkedIn credentials from environment variables
    
    Returns:
        Tuple of (access_token, organization_id) or (None, None) if missing
    """
    
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    organization_id = os.getenv("LINKEDIN_ORGANIZATION_ID")
    
    if not access_token:
        logger.error("LINKEDIN_ACCESS_TOKEN not set in environment variables")
        return None, None
    
    if not organization_id:
        logger.error("LINKEDIN_ORGANIZATION_ID not set in environment variables")
        return None, None
    
    return access_token, organization_id


if __name__ == "__main__":
    # Test the LinkedIn poster
    access_token, org_id = get_linkedin_credentials()
    
    if not access_token or not org_id:
        logger.error("Missing LinkedIn credentials")
        exit(1)
    
    poster = LinkedInPoster(access_token, org_id)
    
    # Test text-only post
    test_post = "Testing LinkedIn automation for CapLinked. This is a test post from our automated system."
    
    logger.info("Sending test post...")
    result = poster.post_text_only(test_post)
    
    if result:
        logger.info(f"Test post successful: {result}")
    else:
        logger.error("Test post failed")
