import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "/etc/secrets/client_secret.json"
TOKEN_PICKLE_FILE = "token.pickle"

def get_authenticated_service( ):
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

def upload_video(youtube_service, video_file_path, title, description, tags):
    print(f"  -> Uploading video to YouTube: '{title}'")
    if not os.path.exists(video_file_path):
        print(f"    ERROR: Video file not found at {video_file_path}")
        return False
    try:
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '22'
            },
            'status': {
                'privacyStatus': 'public'
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
