import os
import pandas as pd
from collections.abc import Callable
from playwright.sync_api import sync_playwright

MAX_RETRIES = 2


class CommonScarper:

    @staticmethod
    def fetch_page(endpoint):
        """Fetches the HTML content of the page (Cloudflare-safe)."""

        tries = 0
        try:
            if tries < MAX_RETRIES:
                return CommonScarper.playwright_fetch_page(endpoint)
            else:
                print("Retried too many times. Stopping...")
        except Exception as e:
            tries += 1
            print(
                f"Error fetching page {endpoint}. Retry {tries} / {MAX_RETRIES}: {e}")
            return CommonScarper.fetch_page(endpoint)

    @staticmethod
    def playwright_fetch_page(endpoint):
        url = f"https://www.basketball-reference.com/{endpoint}"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/127.0.0.0 Safari/537.36",
            )
            page = context.new_page()
            # Try to load and wait for the DOM (not full network)
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                print(f"ERROR: initial load issue at {url}: {e}")
            # Wait a bit for Cloudflare JS challenge to auto-bypass
            page.wait_for_timeout(3100)
            html = page.content()
            browser.close()
            return html

    @staticmethod
    def save_to_csv(df: pd.DataFrame, filename: str):
        """Saves the DataFrame to a CSV file."""
        directory_path = filename.rsplit("/", 1)[0]
        os.makedirs(directory_path, exist_ok=True)

        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    @staticmethod
    def scrape_nba_stats(endpoint: str, output_file: str, parse_statistics_method: Callable, save=True):
        """Main function to scrape stats and save to CSV."""
        html_content = CommonScarper.fetch_page(endpoint)
        if html_content:
            stats_df = parse_statistics_method(html_content)
            if save:
                CommonScarper.save_to_csv(stats_df, output_file)

    @staticmethod
    def scrape_nba_stats_df(endpoint, parse_statistics_method: Callable):
        """Main function to scrape stats and save to CSV."""
        html_content = CommonScarper.fetch_page(endpoint)
        if html_content:
            return parse_statistics_method(html_content)

    @staticmethod
    def scrape_and_save_data(scraper: Callable, endpoint, output_file, save=True):
        CommonScarper.scrape_nba_stats(
            endpoint, output_file, parse_statistics_method=scraper.parse_statistics, save=save)
