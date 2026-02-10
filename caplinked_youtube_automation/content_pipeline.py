import requests
from bs4 import BeautifulSoup
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")
CAPLINKED_BLOG_URL = "https://www.caplinked.com/blog/"

def get_latest_blog_posts(url, limit=3 ):
    print(f"--- Scraping CapLinked blog for latest posts: {url} ---")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("a", class_="blog-card", limit=limit)
        post_urls = []
        for post in posts:
            href = post.get("href")
            if href:
                if not href.startswith("http" ):
                    href = f"https://www.caplinked.com{href}"
                post_urls.append(href )
        print(f"Found {len(post_urls)} new blog posts.")
        return post_urls
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not fetch blog posts. Details: {e}")
        return []

def get_blog_content(url):
    print(f"  -> Scraping content from: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", class_="post-content")
        if content_div:
            for script_or_style in content_div(["script", "style"]):
                script_or_style.decompose()
            text = content_div.get_text(separator="\n", strip=True)
            print(f"    Successfully extracted {len(text)} characters of content.")
            return text
        else:
            print("    ERROR: Could not find the main content div.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"    ERROR: Could not fetch blog content. Details: {e}")
        return None

def generate_video_script(title, content, length_minutes=2):
    print(f"  -> Generating {length_minutes}-minute video script for: '{title}'...")
    if not openai.api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set.")
        return None
    prompt = f"You are a helpful assistant that creates engaging video scripts for a YouTube channel focused on finance, technology, and M&A for an audience of investment bankers, VCs, and corporate development professionals. Your tone should be professional, informative, and concise. Based on the following blog post content, please generate a script for a {length_minutes}-minute video. The script should be structured with a compelling hook, a clear body that explains the key points, and a concise conclusion with a call to action. Blog Post Title: {title}. Blog Post Content: {content[:4000]}. Please generate the complete script now."
    try:
        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
        )
        script = response.choices[0].message.content
        print("    Successfully generated video script.")
        return script
    except Exception as e:
        print(f"    ERROR: Failed to generate script from OpenAI. Details: {e}")
        return None

def run_content_pipeline():
    latest_posts = get_latest_blog_posts(CAPLINKED_BLOG_URL)
    if not latest_posts:
        print("--- Content pipeline finished: No new posts found. ---")
        return []
    video_scripts = []
    for post_url in latest_posts:
        content = get_blog_content(post_url)
        if content:
            title = post_url.split("/")[-2].replace("-", " ").title()
            script = generate_video_script(title, content)
            if script:
                video_scripts.append({
                    "title": f"CapLinked Insights: {title}",
                    "script": script,
                    "source_url": post_url
                })
    print(f"--- Content pipeline finished. Generated {len(video_scripts)} scripts. ---")
    return video_scripts

if __name__ == "__main__":
    run_content_pipeline()
