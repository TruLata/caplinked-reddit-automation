import os
import pickle
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from openai import OpenAI

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "/etc/secrets/client_secret.json"
TOKEN_PICKLE_FILE = "/opt/render/project/src/token.pickle"

# Initialize OpenAI client with explicit API key
api_key = os.environ.get("OPENAI_API_KEY", "" ).strip()
if not api_key:
    print("WARNING: OPENAI_API_KEY not set. SEO metadata generation will use defaults.")
    client = None
else:
    client = OpenAI(api_key=api_key)

def get_authenticated_service():
    credentials = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token_file:
            credentials = pickle.load(token_file)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            print("ERROR: No valid credentials found. Please ensure token.pickle exists.")
            return None
    return build('youtube', 'v3', credentials=credentials)

def generate_seo_metadata(title, script, max_retries=3):
    print(f"    -> Generating SEO-optimized metadata for: {title}")
    
    if not client:
        print(f"    -> OpenAI client not available. Using default metadata.")
        return title, f"Learn more about {title} on the CapLinked blog.", ["CapLinked", "VDR", "M&A", "Finance"]
    
    for attempt in range(max_retries):
        try:
            prompt = f"""Generate SEO-optimized metadata for a YouTube video about: {title}

The video script is: {script[:500]}

Please provide:
1. A compelling YouTube title (60 characters max) that includes keywords about virtual data rooms, M&A, or finance
2. A detailed description (300-500 characters) that includes relevant keywords and a call-to-action
3. 5-10 relevant tags separated by commas

Format your response as:
TITLE: [title]
DESCRIPTION: [description]
TAGS: [tags]"""
            
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500,
                timeout=30
            )
            
            content = response.choices[0].message.content
            lines = content.split('\n')
            
            title_line = next((l for l in lines if l.startswith('TITLE:')), None)
            desc_line = next((l for l in lines if l.startswith('DESCRIPTION:')), None)
            tags_line = next((l for l in lines if l.startswith('TAGS:')), None)
            
            seo_title = title_line.replace('TITLE:', '').strip() if title_line else title
            seo_description = desc_line.replace('DESCRIPTION:', '').strip() if desc_line else f"Learn more about {title} on the CapLinked blog."
            seo_tags = [tag.strip() for tag in tags_line.replace('TAGS:', '').strip().split(',')] if tags_line else ["CapLinked", "VDR", "M&A"]
            
            print(f"    -> SEO metadata generated successfully on attempt {attempt + 1}")
            return seo_title, seo_description, seo_tags
            
        except Exception as e:
            print(f"    ERROR: Failed to generate SEO metadata (attempt {attempt + 1}/{max_retries}). Details: {type(e).__name__}: {e}")
            if attempt < max_retries - 1:
                print(f"    -> Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"    -> Using default metadata")
                # Return default values if all retries fail
                return title, f"Learn more about {title} on the CapLinked blog.", ["CapLinked", "VDR", "M&A", "Finance"]
    
    return title, f"Learn more about {title} on the CapLinked blog.", ["CapLinked", "VDR", "M&A"]

def upload_video(youtube_service, video_file_path, title, script):
    print(f"  -> Uploading video to YouTube: '{title}'")
    if not os.path.exists(video_file_path):
        print(f"    ERROR: Video file not found at {video_file_path}")
        return False
    
    seo_title, seo_description, seo_tags = generate_seo_metadata(title, script)
    
    try:
        body = {
            'snippet': {
                'title': seo_title,
                'description': seo_description,
                'tags': seo_tags,
                'categoryId': '22'
            },
            'status': {
                'privacyStatus': 'public',
                'madeForKids': False
            }
        }
        media = MediaFileUpload(video_file_path, mimetype='video/mp4', resumable=True)
        request = youtube_service.videos().insert(part='snippet,status', body=body, media_body=media)
        response = request.execute()
        video_id = response.get('id')
        print(f"    Successfully uploaded video. Video ID: {video_id}")
        print(f"    Video URL: https://www.youtube.com/watch?v={video_id}" )
        return True
    except Exception as e:
        print(f"    ERROR: Failed to upload video. Details: {e}")
        return False

if __name__ == "__main__":
    print("--- Testing YouTube Uploader ---")
    service = get_authenticated_service()
    if service:
        print("Successfully authenticated with YouTube API.")
    else:
        print("Failed to authenticate with YouTube API.")
