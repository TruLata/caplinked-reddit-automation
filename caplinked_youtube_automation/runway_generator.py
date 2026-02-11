import requests
import os
import time

# Runway API credentials are read from environment variables
RUNWAY_API_KEY = os.environ.get("RUNWAY_API_KEY").strip()
RUNWAY_API_URL = "https://api.dev.runwayml.com/v1"

def generate_video_from_script(script, title ):
    """
    Submits a job to Runway to generate a video from a script and waits for the result.
    NOTE: This is a conceptual implementation. The actual Runway API structure for text-to-video
    may differ. This code assumes an asynchronous job-based workflow.
    """
    print(f"  -> Submitting video generation job to Runway for: '{title}'")

    if not RUNWAY_API_KEY:
        print("    ERROR: RUNWAY_API_KEY environment variable not set.")
        return None

    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json",
        "X-Runway-Version": "2024-11-06"
    }

    # This payload is a simplified example for a text-to-video model.
    # It combines the title and script into a detailed prompt.
    payload = {
        "prompt": f"Create a 2-minute corporate-style video about '{title}'. The video should be informative and visually engaging for a financial professional audience. Use stock footage, motion graphics, and smooth transitions. IMPORTANT: Do NOT include any text overlays, captions, or on-screen text. The video should be purely visual with no text elements. The overall tone should be professional and polished. The script to follow is: {script}",
        "duration_seconds": 120
    }

    try:
        # 1. Submit the generation job
        # The endpoint /text_to_video is the correct Runway endpoint
        response = requests.post(f"{RUNWAY_API_URL}/text_to_video", headers=headers, json=payload)
        response.raise_for_status()
        job_data = response.json()
        job_id = job_data.get("id")

        if not job_id:
            print("    ERROR: Failed to get a job ID from Runway.")
            return None

        print(f"    Successfully submitted job. Job ID: {job_id}. Waiting for completion...")

        # 2. Poll for the result
        while True:
            time.sleep(30) # Poll every 30 seconds
            status_response = requests.get(f"{RUNWAY_API_URL}/jobs/{job_id}", headers=headers)
            status_response.raise_for_status()
            status_data = status_response.json()
            status = status_data.get("status")

            print(f"      Current job status: {status}")

            if status == "succeeded":
                video_url = status_data.get("outputs", [{}])[0].get("url")
                print(f"    Video generation successful. Video URL: {video_url}")
                # In a real scenario, we would download this video file
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
    # For direct testing (will likely fail without a real API key and endpoint)
    print("--- Testing Runway Generator ---")
    test_script = """
    **Scene:** A sleek, modern office with professionals collaborating.
    **Narrator:** In today's fast-paced M&A landscape, efficiency is key.
    **Scene:** Animation showing a virtual data room with secure files.
    **Narrator:** A virtual data room from CapLinked provides the security and tools you need to close deals faster.
    """
    test_title = "The Power of Virtual Data Rooms"
    video_path = generate_video_from_script(test_script, test_title)
    if video_path:
        print(f"Test video generated and saved to: {video_path}")
    else:
        print("Test video generation failed.")
