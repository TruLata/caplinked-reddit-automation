# CapLinked LinkedIn Automation

Fully automated system for posting engaging content to CapLinked's LinkedIn company page.

## Overview

This system:
1. Scrapes the latest blog posts from CapLinked blog
2. Generates engaging LinkedIn posts optimized for GEO/AEO
3. Posts automatically to CapLinked's company page
4. Runs daily via cron job on Render.com

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

### linkedin_poster.py
- Handles authentication with LinkedIn API
- Posts text-only or text+link content
- Manages API requests and error handling
- Supports company page posting

### main.py
- Orchestrates the complete pipeline
- Scrapes -> Generates -> Posts
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

### 2. Generate Access Token

1. Go to https://www.linkedin.com/developers/tools/oauth/token-generator
2. Select your app from dropdown
3. Check all available scopes
4. Click "Request access token"
5. Copy the generated token (valid for 2 months)

### 3. Get Organization ID

1. Visit CapLinked LinkedIn company page
2. Extract ID from URL: linkedin.com/company/{ID}/
3. Or use the API to fetch authenticated user's organizations

### 4. Environment Variables

Set these environment variables in Render.com:

```
OPENAI_API_KEY=your_openai_api_key
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
LINKEDIN_ORGANIZATION_ID=your_organization_id
```

### 5. Deploy on Render.com

1. Connect your GitHub repository
2. Create new Cron Job service
3. Select this directory
4. Set runtime to Python
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `python main.py`
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
```

### Run the automation
```bash
python main.py
```

## Output Files

### linkedin_posts.json
Machine-readable JSON with all posted content:
- Blog title and URL
- Generated LinkedIn post text
- LinkedIn post ID
- Timestamp
- Status (SUCCESS/FAILED)

### linkedin_posting_log.txt
Human-readable log of all posting activities:
- Blog titles and URLs
- Full LinkedIn post text
- Status and post IDs
- Timestamps

### linkedin_automation.log
Detailed technical logs for debugging

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

## API Documentation

- [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
- [LinkedIn OAuth 2.0](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access)
- [OpenAI API](https://platform.openai.com/docs)

## Support

For issues or questions, check the logs:
- `linkedin_automation.log` - Technical logs
- `linkedin_posting_log.txt` - Posting history
- `linkedin_posts.json` - Posted content records
