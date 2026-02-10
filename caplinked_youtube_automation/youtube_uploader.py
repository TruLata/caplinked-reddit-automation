'''
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# In Render, you will create a secret file from your client_secret.json
# and mount it at this path.
CLIENT_SECRETS_FILE = "/etc/secrets/client_secret.json"

# This file stores the user's access and refresh tokens. It must be generated
# once locally and then uploaded to your project so Render can use it.
CREDENTIALS_PICKLE_FILE = "token.pickle"

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    """Authenticates with the YouTube API and returns a service object."""
    credentials = None

    # Check if the token.pickle file exists.
    if os.path.exists(CREDENTIALS_PICKLE_FILE):
        with open(CREDENTIALS_PICKLE_FILE, 'rb') as token:
            credentials = pickle.load(token)
    
    # If there are no valid credentials available, attempt to refresh.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing expired YouTube API access token...")
            try:
                credentials.refresh(Request())
            except Exception as e:
                print(f"ERROR: Could not refresh token. A new authorization may be required. Details: {e}")
                # This indicates the refresh token is likely invalid. The user must re-authenticate locally.
                print("\n---! ACTION REQUIRED !---")
                print("The YouTube refresh token has expired or been revoked.")
                print("You must re-run the authentication process locally to generate a new 'token.pickle' file and upload it to your repository.")
                return None
        else:
            # This block executes if token.pickle is missing or corrupted.
            # It cannot proceed on a server, as it requires interactive login.
            print("\n---! ACTION REQUIRED !---")
            print(f"ERROR: Credentials file '{CREDENTIALS_PICKLE_FILE}' not found or invalid.")
            print("This script must be authenticated to upload videos.")
            print("Please run the 'youtube_uploader.py' script locally on your computer first.")
            print("This will guide you through a browser-based login and create the 'token.pickle' file.")
            print("Once created, you MUST add, commit, and push that file to your GitHub repository for this server to use.")
            return None

        # Save the refreshed credentials for the next run
        with open(CREDENTIALS_PICKLE_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    try:
        print("Successfully authenticated with YouTube API.")
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    except Exception as e:
        print(f"ERROR: Failed to build YouTube service. Details: {e}")
        return None

def upload_video(youtube_service, file_path, title, description, tags):
    """Uploads a video to YouTube."""
    if not youtube_service:
        print("YouTube service is not authenticated. Cannot upload video.")
        return None

    if not os.path.exists(file_path):
        print(f"ERROR: Video file not found at {file_path}. Cannot upload.")
        return None

    print(f"  -> Starting upload for video: {title}")
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '27' # Category 27 is "Education"
        },
        'status': {
            'privacyStatus': 'public' # or 'private' or 'unlisted'
        }
    }

    try:
        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
        request = youtube_service.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"    Uploaded {int(status.progress() * 100)}%")
        
        video_id = response.get('id')
        print(f"  -> Upload successful! Video ID: {video_id}")
        print(f"    Watch on YouTube: https://www.youtube.com/watch?v={video_id}")
        return video_id

    except Exception as e:
        print(f"  ERROR: An error occurred during the upload. Details: {e}")
        return None

if __name__ == '__main__':
    # This main block is for the one-time local authentication.
    print("--- YouTube Uploader Authentication Setup ---")
    print("This script will now attempt to authenticate with Google.")
    
    if not os.path.exists(CLIENT_SECRETS_FILE):
         # Create a dummy file for local run if it doesn't exist
        if not os.path.exists("client_secret.json"):
            print("ERROR: client_secret.json not found.")
            print("Please download your OAuth 2.0 client secrets file from the Google Cloud Console and place it in the same directory as this script.")
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            credentials = flow.run_console()
            with open(CREDENTIALS_PICKLE_FILE, 'wb') as token:
                pickle.dump(credentials, token)
            print(f"\nSUCCESS: Authentication complete. '{CREDENTIALS_PICKLE_FILE}' has been created.")
            print("Please add this file to your GitHub repository.")
    else:
        print("This script is running on a server and expects a pre-existing token.pickle.")
        get_authenticated_service() # Run to test the existing token
'''
