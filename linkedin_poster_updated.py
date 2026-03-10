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
LINKEDIN_API_VERSION = "202506"  # Using June 2025 version (202502 was sunset)

class LinkedInPoster:
    """Handle posting to LinkedIn as a member (for company page)"""
    
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
        self.member_urn = None  # Will be fetched from API
        
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "LinkedIn-Version": LINKEDIN_API_VERSION,
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        # Fetch member ID from API
        self._fetch_member_id()
        logger.info(f"Initialized LinkedIn poster as member: {self.member_urn}")
    
    def _fetch_member_id(self):
        """Fetch authenticated member ID from LinkedIn API"""
        try:
            response = requests.get(
                f"{LINKEDIN_API_BASE}/me",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                member_id = data.get('id')
                self.member_urn = f"urn:li:person:{member_id}"
                logger.info(f"Fetched member ID: {self.member_urn}")
            else:
                logger.error(f"Failed to fetch member ID: {response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching member ID: {e}")
    
    def post_text_only(self, text):
        """
        Post text-only content as member
        
        Args:
            text: Post content (max 3000 characters)
        
        Returns:
            Response from LinkedIn API with post ID
        """
        
        if not self.member_urn:
            logger.error("Member URN not available")
            return None
        
        if len(text) > 3000:
            logger.warning(f"Post text exceeds 3000 characters ({len(text)}), truncating")
            text = text[:2997] + "..."
        
        payload = {
            "author": self.member_urn,
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
    
    def post_with_image(self, text, image_url):
        """
        Post content with image to company page
        
        Args:
            text: Post content
            image_url: URL of image to include
        
        Returns:
            Response from LinkedIn API with post ID
        """
        logger.info("Image posting not yet implemented for member posts")
        return self.post_text_only(text)
    
    def post_blog_content_with_image(self, text, link_url, link_title="", link_description="", image_url=None):
        """
        Post blog content with optional image
        
        Args:
            text: Post commentary
            link_url: URL to blog post
            link_title: Blog post title
            link_description: Blog post description
            image_url: Optional image URL
        
        Returns:
            Response from LinkedIn API with post ID
        """
        
        if not self.member_urn:
            logger.error("Member URN not available")
            return None
        
        if len(text) > 3000:
            logger.warning(f"Post text exceeds 3000 characters ({len(text)}), truncating")
            text = text[:2997] + "..."
        
        payload = {
            "author": self.member_urn,
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
    
    def _make_api_request(self, method, endpoint, data=None):
        """
        Make authenticated request to LinkedIn API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request payload (for POST/PUT)
        
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
            
            else:
                error_msg = response.text
                try:
                    error_data = response.json()
                    error_msg = json.dumps(error_data, indent=2)
                except:
                    pass
                
                logger.error(f"API Error {response.status_code}: {error_msg}")
                return None
        
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

def get_linkedin_credentials():
    """
    Get LinkedIn credentials from environment variables
    
    Returns:
        Tuple of (access_token, organization_id)
    """
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    org_id = os.getenv("LINKEDIN_ORGANIZATION_ID")
    
    if not access_token:
        logger.error("LINKEDIN_ACCESS_TOKEN not set in environment")
    if not org_id:
        logger.error("LINKEDIN_ORGANIZATION_ID not set in environment")
    
    return access_token, org_id
