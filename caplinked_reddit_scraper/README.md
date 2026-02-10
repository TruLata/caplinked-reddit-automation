# Reddit Monitoring System (Web Scraping)

This system monitors specified subreddits for relevant keywords using web scraping. It does not use the Reddit API and is designed to be compliant with Reddit's terms of service for crawling public content.

## How It Works

1.  **Scrapes Public Pages:** The `reddit_scraper.py` script sends HTTP requests to the "new" page of each target subreddit.
2.  **Parses HTML:** It uses BeautifulSoup to parse the HTML and find post containers.
3.  **Keyword Matching:** It checks post titles for keywords defined in the script.
4.  **Generates Report:** It saves any matches to a `reddit_monitoring_results.json` file.

## How to Use

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Scraper:**
    ```bash
    python3 reddit_scraper.py
    ```
3.  **Review Results:** Check the `reddit_monitoring_results.json` file for any relevant posts.

## Configuration

-   **Subreddits:** Edit the `SUBREDDITS` list in `reddit_scraper.py` to change which subreddits are monitored.
-   **Keywords:** Edit the `KEYWORDS` list to change the search terms.
