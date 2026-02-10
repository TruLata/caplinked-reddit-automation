# YouTube Automation System

This system automates the process of creating and uploading YouTube videos from CapLinked's blog content.

## How It Works

1.  **Content Pipeline (`content_pipeline.py`):**
    *   Scrapes the CapLinked blog for the latest posts.
    *   Extracts the text content from each post.
    *   Uses OpenAI's GPT-4 to generate a 2-3 minute video script from the content.

2.  **Video Generation (`runway_generator.py`):**
    *   Sends the generated script to the RunwayML API to create a video.
    *   Monitors the generation status and downloads the video when complete.

3.  **YouTube Upload (`youtube_uploader.py`):**
    *   Uses the YouTube Data API to upload the generated video.
    *   Sets the title, description, and other metadata.
    *   Can be configured to schedule the video for a specific time.

## How to Use

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Configure APIs:**
    *   **OpenAI:** Set your `OPENAI_API_KEY` environment variable.
    *   **RunwayML:** Add your API key to `runway_generator.py`.
    *   **YouTube:** Follow the instructions in the [Google Cloud documentation](https://developers.google.com/youtube/v3/quickstart/python) to create a `client_secret.json` file.
3.  **Run the Pipeline:**
    *   Run `content_pipeline.py` to generate a script.
    *   Run `runway_generator.py` to create the video.
    *   Run `youtube_uploader.py` to upload the video.

## Review Dashboard (Conceptual)

A web-based dashboard will be created to allow for human review of the generated videos before they are uploaded. This will provide a final quality control point to ensure quality and brand alignment.
