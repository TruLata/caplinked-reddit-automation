import requests
import os
import time

RUNWAY_API_KEY = os.environ.get("RUNWAY_API_KEY", "").strip()
RUNWAY_API_URL = "https://api.runwayml.com/v1"

def generate_video_from_script(script, title ):
    print(f"  -> Submitting video generation job to Runway for: '{title}'")
    if not RUNWAY_API_KEY:
        print("    ERROR: RUNWAY_API_KEY environment variable not set.")
        return None
    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"Create a 2-minute corporate-style video about '{title}'. The video should be informative and visually engaging for a financial professional audience. Use stock footage, motion graphics, and clear on-screen text. The overall tone should be professional and polished. The script to follow is: {script}",
        "duration_seconds": 120
    }
    try:
        response = requests.post(f"{RUNWAY_API_URL}/generate", headers=headers, json=payload)
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
            status_response = requests.get(f"{RUNWAY_API_URL}/jobs/{job_id}", headers=headers)
            status_response.raise_for_status()
            status_data = status_response.json()
            status = status_data.get("status")
            print(f"    Job status: {status}")
            if status == "succeeded":
                video_url = status_data.get("outputs", [{}])[0].get("url")
                print(f"    Video generation successful. Video URL: {video_url}")
                video_content = requests.get(video_url).content
                file_path = f"/tmp/{title.replace(' ', '_')}.mp4"
                with open(file_path, 'wb') as f:
                    f.write(video_content)
                print(f"    Video downloaded to: {file_path}")
                return file_path
            elif status in ["failed", "timed_out"]:
                print(f"    ERROR: Video generation failed with status: {status}")
                return None
    except requests.exceptions.RequestException as e:
        print(f"    ERROR: An error occurred with the Runway API. Details: {e}")
        print("    NOTE: This may be due to the hypothetical nature of the API endpoint.")
        return None

if __name__ == "__main__":
    print("--- Testing Runway Generator ---")
    test_script = "**Scene:** A sleek, modern office with professionals collaborating. **Narrator:** In today's fast-paced M&A landscape, efficiency is key."
    test_title = "The Power of Virtual Data Rooms"
    video_path = generate_video_from_script(test_script, test_title)
    if video_path:
        print(f"Test video generated and saved to: {video_path}")
    else:
        print("Test video generation failed.")
