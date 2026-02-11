import requests
import os
import time

RUNWAY_API_KEY = os.environ.get("RUNWAY_API_KEY", "").strip()
RUNWAY_API_URL = "https://api.dev.runwayml.com/v1"
RUNWAY_API_VERSION = "2024-11-06"

def generate_video_from_script(script, title  ):
    print(f"  -> Submitting video generation job to Runway for: '{title}'")
    if not RUNWAY_API_KEY:
        print("    ERROR: RUNWAY_API_KEY environment variable not set.")
        return None
    
    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json",
        "X-Runway-Version": RUNWAY_API_VERSION
    }
    
    # Add the "NO TEXT OVERLAYS" instruction to the script
    enhanced_script = f"IMPORTANT: Do NOT include any text overlays, captions, or on-screen text. The video should be purely visual with no text elements. {script[:900]}"
    
    payload = {
        "model": "veo3.1",
        "promptText": enhanced_script,
        "ratio": "1280:720",
        "duration": 8,
        "audio": True
    }
    
    try:
        response = requests.post(f"{RUNWAY_API_URL}/text_to_video", headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        job_data = response.json()
        job_id = job_data.get("id")
        if not job_id:
            print("    ERROR: Failed to get a job ID from Runway.")
            return None
        print(f"    Successfully submitted job. Job ID: {job_id}. Waiting for video generation...")
        
        max_wait_time = 600
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            time.sleep(10)
            status_response = requests.get(f"{RUNWAY_API_URL}/tasks/{job_id}", headers=headers, timeout=30)
            status_response.raise_for_status()
            status_data = status_response.json()
            status = status_data.get("status")
            print(f"    Job status: {status}")
            if status == "SUCCEEDED":
                output = status_data.get("output")
                if output:
                    video_url = output[0] if isinstance(output, list) else (output if isinstance(output, str) else output.get("url"))
                    print(f"    Video generation successful. Video URL: {video_url}")
                    video_content = requests.get(video_url).content
                    file_path = f"/tmp/{title.replace(' ', '_')}.mp4"
                    with open(file_path, 'wb') as f:
                        f.write(video_content)
                    print(f"    Video downloaded to: {file_path}")
                    return file_path
            elif status in ["FAILED", "TIMED_OUT"]:
                print(f"    ERROR: Video generation failed with status: {status}")
                return None
        print("    ERROR: Video generation timed out after 10 minutes.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"    ERROR: An error occurred with the Runway API. Details: {e}")
        return None

if __name__ == "__main__":
    print("--- Testing Runway Generator ---")
    test_script = "A sleek, modern office with professionals collaborating. In today's fast-paced M&A landscape, efficiency is key."
    test_title = "The Power of Virtual Data Rooms"
    video_path = generate_video_from_script(test_script, test_title)
    if video_path:
        print(f"Test video generated and saved to: {video_path}")
    else:
        print("Test video generation failed.")
