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

# Use parent logger from main script
logger = logging.getLogger(__name__)

# LinkedIn API Configuration - CORRECT ENDPOINT
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
        self.member_urn = member_urn  # Will use ~ (authenticated user) if not provided
        
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
            Post ID if successful, None otherwise
        """
        
        if len(text) > 3000:
            logger.warning(f"Post text exceeds 3000 characters ({len(text)}), truncating")
            text = text[:2997] + "..."
        
        # Correct payload format from official LinkedIn API docs
        payload = {
            "author": "urn:li:person:~",  # Tilde represents authenticated user
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }
        
        return self._make_api_request("POST", "/posts", payload)
    
    def post_with_link(self, text, link_url, link_title="", link_description=""):
        """
        Post content with a link/article as member
        
        Args:
            text: Post commentary
            link_url: URL to include
            link_title: Title for the article
            link_description: Description for the article
        
        Returns:
            Post ID if successful, None otherwise
        """
        
        if len(text) > 3000:
            logger.warning(f"Post text exceeds 3000 characters ({len(text)}), truncating")
            text = text[:2997] + "..."
        
        # Correct payload format for article post from official LinkedIn API docs
        payload = {
            "author": "urn:li:person:~",  # Tilde represents authenticated user
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "content": {
                "article": {
                    "source": link_url,
                    "title": link_title[:200] if link_title else "",
                    "description": link_description[:200] if link_description else ""
                }
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }
        
        return self._make_api_request("POST", "/posts", payload)
    
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
            # Log request details for debugging
            logger.debug(f"API Request: {method} {url}")
            logger.debug(f"Headers: {self.headers}")
            logger.debug(f"Payload: {json.dumps(data, indent=2) if data else 'None'}")
            
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
        
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None


def get_linkedin_credentials():
    """
    Get LinkedIn credentials from environment variables
    
    Returns:
        Tuple of (access_token, member_urn)
    """
    
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    member_urn = os.getenv("LINKEDIN_MEMBER_URN")
    
    if not access_token:
        logger.error("LINKEDIN_ACCESS_TOKEN environment variable not set")
        return None, None
    
    if member_urn:
        logger.info(f"Using member URN: {member_urn}")
    else:
        logger.warning("LINKEDIN_MEMBER_URN not set - will use authenticated user")
    
    return access_token, member_urn
