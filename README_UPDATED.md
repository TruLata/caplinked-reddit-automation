# CapLinked LinkedIn Automation (Updated with Image Generation)

Fully automated system for posting engaging content with AI-generated images to CapLinked's LinkedIn company page.

## Overview

This system:
1. Scrapes the latest blog posts from CapLinked blog
2. Generates engaging LinkedIn posts optimized for GEO/AEO
3. Generates professional images using Runway AI
4. Posts automatically to CapLinked's company page with images
5. Runs daily via cron job on Render.com

## New Features

### Image Generation
- Uses Runway AI to generate professional LinkedIn images
- Optimized dimensions (1200x630px) for LinkedIn
- Images include relevant visual themes based on blog content
- Professional corporate design with CapLinked brand colors
- Significantly improves engagement (images get 10x more engagement)

## Components

### blog_scraper.py
- Fetches latest blog posts from caplinked.com/blog
- Extracts title, excerpt, and URL
- Returns structured post data

### linkedin_post_generator.py
- Generates engaging LinkedIn posts using OpenAI GPT-4.1-mini
- Optimized for GEO/AEO (Google E-E-A-T and AI search visibility)
- Targets finance professionals and M&A professionals
- Includes keywords for search visibility
- Generates posts under 1300 characters for optimal engagement

### image_generator.py (NEW)
- Generates professional images using Runway AI
- Creates images optimized for LinkedIn (1200x630px)
- Includes visual themes related to blog content
- Professional corporate aesthetic
- Supports fallback if image generation fails

### linkedin_poster_updated.py
- Handles authentication with LinkedIn API
- Posts text+image or text+link content
- Manages API requests and error handling
- Supports company page posting

### main_updated.py
- Orchestrates the complete pipeline
- Scrapes -> Generates Post -> Generates Image -> Posts
- Logs all activities
- Saves results to JSON and text files

## Setup Instructions

### 1. LinkedIn Developer App Setup

1. Go to https://www.linkedin.com/developers/apps/new
2. Create a new app associated with CapLinked company page
3. In Settings tab, verify your app
4. In Products tab, enable:
   - Share on LinkedIn
   - Sign In with LinkedIn using OpenID Connect
5. In Auth tab, note the required OAuth 2.0 scopes

### 2. Generate LinkedIn Access Token

1. Go to https://www.linkedin.com/developers/tools/oauth/token-generator
2. Select your app from dropdown
3. Check all available scopes
4. Click "Request access token"
5. Copy the generated token (valid for 2 months)

### 3. Get Organization ID

1. Visit CapLinked LinkedIn company page
2. Extract ID from URL: linkedin.com/company/{ID}/
3. Or use the API to fetch authenticated user's organizations

### 4. Get Runway AI API Key

1. Go to https://www.runwayml.com
2. Sign up for an account
3. Go to API section
4. Generate an API key
5. Save it securely

### 5. Environment Variables

Set these environment variables in Render.com:

```
OPENAI_API_KEY=your_openai_api_key
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
LINKEDIN_ORGANIZATION_ID=your_organization_id
RUNWAY_API_KEY=your_runway_api_key
```

### 6. Deploy on Render.com

1. Connect your GitHub repository
2. Create new Cron Job service
3. Select this directory
4. Set runtime to Python
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `python main_updated.py`
7. Set schedule: `0 11 * * *` (daily at 11 AM UTC)
8. Add environment variables
9. Deploy

## Local Testing

### Install dependencies
```bash
pip install -r requirements.txt
```

### Set environment variables
```bash
export OPENAI_API_KEY=your_key
export LINKEDIN_ACCESS_TOKEN=your_token
export LINKEDIN_ORGANIZATION_ID=your_id
export RUNWAY_API_KEY=your_runway_key
```

### Run the automation
```bash
python main_updated.py
```

## Output Files

### linkedin_posts.json
Machine-readable JSON with all posted content:
- Blog title and URL
- Generated LinkedIn post text
- Generated image URL
- LinkedIn post ID
- Timestamp
- Status (SUCCESS/FAILED)

### linkedin_posting_log.txt
Human-readable log of all posting activities:
- Blog titles and URLs
- Full LinkedIn post text
- Image URLs
- Status and post IDs
- Timestamps

### linkedin_automation.log
Detailed technical logs for debugging

## Image Generation Details

### How It Works
1. Blog content is analyzed for relevant themes
2. Runway AI generates a professional image based on the blog topic
3. Image is optimized for LinkedIn (1200x630px)
4. Image URL is included in the LinkedIn post

### Image Themes
The system automatically selects visual themes based on blog keywords:
- VDR: Secure data storage, digital documents, cloud security
- M&A: Business deal, handshake, corporate growth, merger
- Due Diligence: Magnifying glass, analysis, investigation, research
- Compliance: Checkmark, compliance, security, regulations
- Fundraising: Growth chart, investment, capital, funding
- Investment Banking: Financial charts, stock market, trading

### Fallback Behavior
If image generation fails:
- Post still goes to LinkedIn with text only
- No delay or failure of entire post
- Logged for monitoring

## Token Refresh

LinkedIn access tokens expire after 2 months. You'll need to:
1. Generate a new token from the developer portal
2. Update the LINKEDIN_ACCESS_TOKEN environment variable in Render.com
3. Restart the cron job

## Content Strategy

The system generates posts that:
- Appeal to finance professionals and M&A advisors
- Include keywords for search visibility (VDR, M&A, due diligence, etc.)
- Provide value and insights
- Include natural call-to-action with blog link
- Maintain professional but conversational tone
- Optimize for GEO/AEO (Google E-E-A-T and AI search)

Posts are paired with professional images that:
- Increase engagement by 10x compared to text-only
- Maintain professional corporate aesthetic
- Include relevant visual themes
- Use CapLinked brand colors
- Are optimized for LinkedIn dimensions

## Troubleshooting

### No posts found
- Check if CapLinked blog is accessible
- Verify blog HTML structure hasn't changed
- Update CSS selectors in blog_scraper.py if needed

### LinkedIn API errors
- Verify access token is valid (not expired)
- Check organization ID is correct
- Ensure app has required permissions
- Check rate limiting (max 1 post per minute)

### Post generation issues
- Verify OpenAI API key is valid
- Check OpenAI account has available credits
- Review generated post in logs for quality

### Image generation issues
- Verify Runway API key is valid
- Check Runway account has available credits
- Review image generation logs for errors
- System will post without image if generation fails

## API Documentation

For reference:
- [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
- [LinkedIn OAuth 2.0](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access)
- [OpenAI API](https://platform.openai.com/docs)
- [Runway AI API](https://docs.runwayml.com/)

## Support

If you encounter issues:

1. Check the logs in Render dashboard
2. Review the README.md in the automation directory
3. Verify all environment variables are correctly set
4. Ensure LinkedIn token hasn't expired
5. Test the blog scraper locally to verify blog access
6. Check Runway API key is valid for image generation

## File Structure

```
caplinked_linkedin_automation/
├── main_updated.py                 # Main orchestration script (with images)
├── blog_scraper.py                 # Blog content extraction
├── linkedin_post_generator.py      # AI post generation
├── image_generator.py              # Runway AI image generation (NEW)
├── linkedin_poster_updated.py      # LinkedIn API integration (updated)
├── requirements.txt                # Python dependencies
├── render.yaml                     # Render deployment config
└── README_UPDATED.md               # This documentation
```

## Performance

Typical execution time per run:
- Blog scraping: 5-10 seconds
- Post generation: 10-15 seconds
- Image generation: 30-60 seconds (Runway AI)
- LinkedIn posting: 5-10 seconds
- Total: 50-95 seconds per run

## Cost Considerations

- OpenAI API: ~$0.01-0.02 per post
- Runway AI: ~$0.10-0.20 per image
- LinkedIn API: Free
- Total cost per day: ~$0.20-0.40 (2 posts with images)

## Next Steps

1. Complete setup with all environment variables
2. Deploy to Render.com
3. Monitor the first few runs
4. Adjust image generation prompts if needed
5. Set calendar reminder for LinkedIn token refresh (2 months)
