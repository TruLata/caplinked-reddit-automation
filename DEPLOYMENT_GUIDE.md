# CapLinked Automation Suite - Deployment Guide

This guide provides step-by-step instructions for deploying the Reddit, Quora, and YouTube automation systems to your Cloudways server.

## 1. Deploy Code to Cloudways

1.  **Push to GitHub:** Ensure all the code in this repository is pushed to your GitHub account.
2.  **Connect to Cloudways:** In your Cloudways dashboard, connect your GitHub repository using the "Deployment via GIT" feature.
3.  **Deploy:** Click "Start Deployment" to pull the latest code to your server.

## 2. Install Dependencies

Once the code is deployed, you will need to install the Python dependencies for each system. Since we cannot run shell commands directly, we will use a PHP script to do this.

1.  **Upload `setup.php`:** A `setup.php` file is included in this repository. Make sure it is deployed to your `public_html` directory.
2.  **Run Setup Script:** Visit `https://your-cloudways-domain.com/setup.php` in your browser. This will install all the necessary Python packages.

## 3. Configure API Keys

You will need to create a `config.json` file in the `caplinked_youtube_automation` directory with your API keys.

1.  **Create `config.json`:**
    ```json
    {
        "openai_api_key": "YOUR_OPENAI_API_KEY",
        "runway_api_key": "YOUR_RUNWAY_API_KEY",
        "youtube_client_secret_file": "client_secret.json"
    }
    ```
2.  **Add YouTube `client_secret.json`:** Follow the Google Cloud documentation to generate your `client_secret.json` file and place it in the `caplinked_youtube_automation` directory.

## 4. Set Up Cron Jobs

To run the monitoring scripts automatically, you need to set up cron jobs in your Cloudways dashboard.

1.  **Go to Cron Job Management:** In your Cloudways dashboard, find the "Cron Job Management" section.
2.  **Add Cron Jobs:**
    *   **Reddit Scraper:**
        *   **Schedule:** Every 6 hours (`0 */6 * * *`)
        *   **Command:** `cd /home/your_user/public_html/caplinked_reddit_scraper && python3 reddit_scraper.py`
    *   **Quora Scraper:**
        *   **Schedule:** Every 6 hours (`0 */6 * * *`)
        *   **Command:** `cd /home/your_user/public_html/caplinked_quora_scraper && python3 quora_scraper.py`
    *   **YouTube Automation:**
        *   **Schedule:** 3 times a week (e.g., `0 9 * * 1,3,5` for Mon, Wed, Fri at 9am)
        *   **Command:** `cd /home/your_user/public_html/caplinked_youtube_automation && python3 content_pipeline.py && python3 runway_generator.py && python3 youtube_uploader.py`

## 5. Access the Dashboard

Once the scrapers have run, you can view the results on the unified dashboard.

1.  **Run the Dashboard:**
    ```bash
    cd /home/your_user/public_html/caplinked_dashboard
    python3 dashboard.py
    ```
2.  **Access in Browser:** The dashboard will be available at `http://your-cloudways-domain.com:8080`.
