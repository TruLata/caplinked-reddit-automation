# Quora Monitoring System (Web Scraping)

This system monitors Quora for relevant questions using web scraping. It does not use an API and is designed to be compliant with Quora's terms of service for crawling public content for informational purposes.

## How It Works

1.  **Scrapes Search Results:** The `quora_scraper.py` script sends HTTP requests to Quora's search results page for each specified keyword.
2.  **Parses HTML:** It uses BeautifulSoup to parse the HTML and find question containers.
3.  **Extracts Questions:** It extracts the question text and link.
4.  **Generates Report:** It saves any found questions to a `quora_monitoring_results.json` file.

## How to Use

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Scraper:**
    ```bash
    python3 quora_scraper.py
    ```
3.  **Review Results:** Check the `quora_monitoring_results.json` file for any relevant questions.

## Configuration

-   **Keywords:** Edit the `KEYWORDS` list in `quora_scraper.py` to change the search terms.
