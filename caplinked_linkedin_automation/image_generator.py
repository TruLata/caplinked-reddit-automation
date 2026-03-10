"""
Image Generator for LinkedIn Posts
Uses Runway AI to generate relevant images for LinkedIn content
"""

import requests
import logging
import os
import time
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

RUNWAY_API_BASE = "https://api.dev.runwayml.com/v1"
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")

class LinkedInImageGenerator:
    """Generate images for LinkedIn posts using Runway AI"""
    
    def __init__(self):
        """Initialize image generator with Runway API key"""
        self.api_key = RUNWAY_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Runway-Version": "2024-11-15"
        }
        
        if not self.api_key:
            logger.warning("RUNWAY_API_KEY not set - image generation disabled")
        else:
            logger.info("Initialized Runway AI image generator")
    
    def generate_image(self, prompt, blog_title=""):
        """
        Generate an image using Runway AI
        
        Args:
            prompt: Image generation prompt
            blog_title: Blog title for logging
        
        Returns:
            URL to generated image or None if failed
        """
        
        if not self.api_key:
            logger.warning("Runway API key not configured")
            return None
        
        try:
            logger.info(f"Generating image for: {blog_title}")
            
            # Runway AI image generation request
            payload = {
                "model": "gen3",
                "prompt": prompt,
                "width": 1200,
                "height": 630,  # LinkedIn optimal image size
                "num_images": 1,
                "steps": 30,
                "guidance_scale": 7.5
            }
            
            response = requests.post(
                f"{RUNWAY_API_BASE}/image_generation",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if "image_url" in result:
                    image_url = result["image_url"]
                    logger.info(f"Successfully generated image: {image_url}")
                    return image_url
                elif "images" in result and len(result["images"]) > 0:
                    image_url = result["images"][0]["url"]
                    logger.info(f"Successfully generated image: {image_url}")
                    return image_url
                else:
                    logger.error(f"Unexpected response format: {result}")
                    return None
            
            elif response.status_code == 429:
                logger.warning("Rate limited by Runway API")
                return None
            
            else:
                logger.error(f"Image generation failed: {response.status_code} - {response.text}")
                return None
        
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None
    
    def generate_linkedin_image(self, blog_title, blog_excerpt, topic="VDR"):
        """
        Generate a professional LinkedIn image for blog content
        
        Args:
            blog_title: Title of the blog post
            blog_excerpt: Excerpt from the blog post
            topic: Topic for image generation (VDR, M&A, Finance, etc.)
        
        Returns:
            URL to generated image or None
        """
        
        # Create a professional prompt for Runway AI
        prompt = f"""Create a professional, modern LinkedIn image (1200x630px) for a blog post about {topic}.

Blog Title: {blog_title}
Blog Excerpt: {blog_excerpt[:150]}

Requirements:
- Professional corporate design
- Modern, clean aesthetic
- Include relevant icons or graphics related to {topic}
- Use CapLinked brand colors (green and dark blue)
- Include subtle text overlay with key topic
- High quality, suitable for LinkedIn
- No people in the image
- Avoid text that's too small to read
- Modern, minimalist design

Style: Professional corporate, modern, clean, trustworthy"""
        
        return self.generate_image(prompt, blog_title)
    
    def download_image(self, image_url, filename):
        """
        Download generated image to local storage
        
        Args:
            image_url: URL of the image
            filename: Local filename to save as
        
        Returns:
            Local file path if successful, None otherwise
        """
        
        try:
            logger.info(f"Downloading image to {filename}")
            
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                logger.info(f"Image saved to {filename}")
                return filename
            else:
                logger.error(f"Failed to download image: {response.status_code}")
                return None
        
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            return None


def generate_image_prompt_from_blog(blog_title, blog_excerpt, keywords=None):
    """
    Generate an optimized image prompt from blog content
    
    Args:
        blog_title: Blog post title
        blog_excerpt: Blog excerpt
        keywords: List of keywords from the blog
    
    Returns:
        Optimized prompt for image generation
    """
    
    # Map keywords to visual themes
    visual_themes = {
        "VDR": "secure data storage, digital documents, cloud security",
        "M&A": "business deal, handshake, corporate growth, merger",
        "due diligence": "magnifying glass, analysis, investigation, research",
        "compliance": "checkmark, compliance, security, regulations",
        "fundraising": "growth chart, investment, capital, funding",
        "investment banking": "financial charts, stock market, trading",
        "deal management": "business process, workflow, management",
        "data room": "secure vault, digital storage, documents"
    }
    
    # Find matching theme
    theme = "professional finance"
    if keywords:
        for keyword in keywords:
            if keyword.lower() in visual_themes:
                theme = visual_themes[keyword.lower()]
                break
    
    prompt = f"""Professional LinkedIn image (1200x630px) for finance/business blog post.

Title: {blog_title}
Theme: {theme}

Design requirements:
- Modern, professional corporate aesthetic
- Clean, minimalist layout
- Incorporate visual elements related to: {theme}
- Use professional colors (blues, greens, grays)
- High quality, suitable for LinkedIn
- No people or faces
- Include subtle branding elements
- Text overlay with key concept from title
- Modern sans-serif typography
- Trustworthy, authoritative appearance"""
    
    return prompt


if __name__ == "__main__":
    # Test image generator
    generator = LinkedInImageGenerator()
    
    test_title = "VDRs As Compliance Command Centers"
    test_excerpt = "Virtual data rooms serve as centralized compliance hubs for M&A transactions"
    
    print("Generating test image...")
    image_url = generator.generate_linkedin_image(test_title, test_excerpt, "VDR")
    
    if image_url:
        print(f"Generated image URL: {image_url}")
        
        # Try to download
        filename = f"test_image_{int(time.time())}.png"
        local_path = generator.download_image(image_url, filename)
        
        if local_path:
            print(f"Image saved to: {local_path}")
    else:
        print("Image generation failed")
