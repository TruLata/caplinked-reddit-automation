"""
LinkedIn API Integration for CapLinked
Posts generated content as member (tracewellgordon) with CapLinked organization mention
User can then manually share to CapLinked company page
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
LINKEDIN_API_VERSION = "202506"

# CapLinked organization URN for mentions
CAPLINKED_ORG_URN = "urn:li:organization:739542"

class LinkedInMemberPoster:
    """Handle posting to LinkedIn as member with organization mention"""
    
    def __init__(self, access_token, member_urn=None):
        """
        Initialize LinkedIn member poster
        
        Args:
            access_token: LinkedIn OAuth access token with w_member_social scope
            member_urn: Member URN (optional, will use authenticated user if not provided)
        """
        self.access_token = access_token
        self.member_urn = member_urn  # Will be fetched if not provided
        
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Linkedin-Version": LINKEDIN_API_VERSION,
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        logger.info("Initialized LinkedIn member poster")
    
    def post_text_only(self, text):
        """
        Post text-only content as member
        
        Args:
            text: Post content (max 3000 characters)
        
        Returns:
            Response from LinkedIn API with post ID
        """
        
        if len(text) > 3000:
            logger.warning(f"Post text exceeds 3000 characters ({len(text)}), truncating")
            text = text[:2997] + "..."
        
        # Use authenticated user as author
        payload = {
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
    
    def post_with_link(self, text, link_url, link_title="", link_description=""):
        """
        Post content with a link preview as member
        
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
                logger.error("Forbidden - May lack required permissions (w_member_social)")
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
    
    def post_blog_content(self, blog_title, post_text, blog_url):
        """
        Post blog content with link to LinkedIn as member
        
        Args:
            blog_title: Title of the blog post
            post_text: Generated post text (should already include CapLinked mention)
            blog_url: URL to the blog post
        
        Returns:
            Post ID if successful, None otherwise
        """
        
        try:
            logger.info(f"Posting to LinkedIn as member: {blog_title}")
            
            result = self.post_with_link(
                text=post_text,
                link_url=blog_url,
                link_title=blog_title,
                link_description="Read the full article on CapLinked blog"
            )
            
            if result and "id" in result:
                post_id = result["id"]
                logger.info(f"Successfully posted to LinkedIn. Post ID: {post_id}")
                logger.info(f"Post can now be manually shared to CapLinked company page")
                return post_id
            else:
                logger.error("Failed to get post ID from response")
                return None
        
        except Exception as e:
            logger.error(f"Error posting blog content: {e}")
            return None


def get_linkedin_credentials():
    """
    Get LinkedIn credentials from environment variables
    
    Returns:
        Tuple of (access_token, member_urn) or (None, None) if missing
    """
    
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    member_urn = os.getenv("LINKEDIN_MEMBER_URN")
    
    if not access_token:
        logger.error("LINKEDIN_ACCESS_TOKEN not set in environment variables")
        return None, None
    
    # Member URN is optional - will use authenticated user if not provided
    if not member_urn:
        logger.warning("LINKEDIN_MEMBER_URN not set - will use authenticated user")
    
    return access_token, member_urn


if __name__ == "__main__":
    # Test the LinkedIn member poster
    access_token, member_urn = get_linkedin_credentials()
    
    if not access_token:
        logger.error("Missing LinkedIn access token")
        exit(1)
    
    poster = LinkedInMemberPoster(access_token, member_urn)
    
    # Test text-only post with CapLinked mention
    test_post = """Exploring the latest insights on VDR best practices and M&A due diligence. 

What makes a data room truly secure? The answer lies in comprehensive access controls, audit trails, and intelligent document management.

Learn more about securing your M&A process with CapLinked's virtual data room solutions. 

On behalf of CapLinked"""
    
    logger.info("Sending test post...")
    result = poster.post_text_only(test_post)
    
    if result:
        logger.info(f"Test post successful: {result}")
        logger.info("You can now manually share this post to CapLinked's company page")
    else:
        logger.error("Test post failed")
