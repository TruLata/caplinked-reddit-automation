import requests
from bs4 import BeautifulSoup
import openai
import os
import textwrap

# Configure OpenAI API
# The API key is read from an environment variable for security.
openai.api_key = os.environ.get("OPENAI_API_KEY")

CAPLINKED_BLOG_URL = "https://www.caplinked.com/blog/"

def get_latest_blog_posts(url, limit=3 ):
    """Fetches the latest blog posts from the CapLinked blog."""
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
    """Extracts the main text content from a single blog post."""
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
    """Generates a video script from blog content using OpenAI."""
    print(f"  -> Generating {length_minutes}-minute video script for: '{title}'...")
    
    if not openai.api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set.")
        return None

    # The textwrap.dedent function removes common leading whitespace
    # from every line in a string, fixing the indentation issue.
    prompt = textwrap.dedent(f'''
        You are a helpful assistant that creates engaging video scripts for a YouTube channel focused on finance, technology, and M&A for an audience of investment bankers, VCs, and corporate development professionals. Your tone should be professional, informative, and concise.

        Based on the following blog post content, please generate a script for a {length_minutes}-minute video. The script should be structured with a compelling hook, a clear body that explains the key points, and a concise conclusion with a call to action (e.g., "subscribe for more insights").

        IMPORTANT: Do NOT include any text overlays, captions, or on-screen text in the video. The video should be purely visual with voiceover narration. Focus on:
        - Visual descriptions (animations, graphics, stock footage, transitions)
        - Narrator voiceover (clear, professional, engaging)
        - NO text, titles, or captions to be displayed on screen

        The script should be formatted with scene descriptions and narrator voiceover text clearly separated. For example:

        **Scene:** [Description of a visual, e.g., "Abstract animation of data flowing between servers"]
        **Narrator:** [Voiceover text, e.g., "In the world of high-stakes deals, security is paramount."]

        **Blog Post Title:** {title}
        **Blog Post Content:**
        --- 
        {content[:4000]}  # Use the first 4000 characters to stay within token limits
        --- 

        Please generate the complete script now. Remember: NO on-screen text or captions - only visual elements and voiceover.
        ''')

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
    """The main function to run the full content-to-script pipeline."""
    latest_posts = get_latest_blog_posts(CAPLINKED_BLOG_URL)
    if not latest_posts:
        print("--- Content pipeline finished: No new posts found. ---\n")
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
    
    print(f"--- Content pipeline finished. Generated {len(video_scripts)} scripts. ---\n")
    return video_scripts

if __name__ == "__main__":
    run_content_pipeline()
