import os
from .content_pipeline import run_content_pipeline
from .runway_generator import generate_video_from_script
from .youtube_uploader import get_authenticated_service, upload_video

def main():
    """Main orchestrator for the entire YouTube automation pipeline."""
    print("--- Starting YouTube Automation Pipeline ---")
    # 1. Generate video scripts from blog posts
    scripts_data = run_content_pipeline()
    if not scripts_data:
        print("--- Pipeline finished: No scripts were generated. ---")
        return
    # 2. Authenticate with YouTube
    print("--- Authenticating with YouTube ---")
    youtube_service = get_authenticated_service()
    if not youtube_service:
        print("--- Pipeline aborted: Could not authenticate with YouTube. ---")
        print("Please ensure a valid 'token.pickle' file exists in the repository.")
        return
    # 3. Generate and upload videos for each script
    for video_data in scripts_data:
        title = video_data["title"]
        script = video_data["script"]
        source_url = video_data["source_url"]
        print(f"--- Processing script for: {title} ---")
        # a. Generate video using Runway AI
        # NOTE: This is a placeholder. The Runway API part is conceptual.
        # In a real scenario, you'd get a file path back.
        video_path = generate_video_from_script(script, title)
        if not video_path:
            print(f"  -> Skipping upload for [33m'{title}'[0m as video generation failed.")
            continue
        # b. Upload the generated video to YouTube
        description = f"An overview of '{title}'. Learn more on the CapLinked blog: {source_url}\n\nThis video was generated as part of an automated content marketing initiative."
        tags = ["CapLinked", "VDR", "Virtual Data Room", "M&A", "Due Diligence", "Fintech"] + title.split()
        
        upload_video(youtube_service, video_path, title, description, tags)
    print("--- YouTube Automation Pipeline Finished ---")

if __name__ == "__main__":
    main()
