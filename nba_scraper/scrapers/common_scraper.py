import requests
import os
import time
import pandas as pd
from collections.abc import Callable


class CommonScarper:

    @staticmethod
    def fetch_page(endpoint):
        """Fetches the HTML content of the page."""
        url = f"https://www.basketball-reference.com/{endpoint}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        if response.status_code == 404:
            print(f"Can't find URL {url}")
        else:
            print(
                f"Error: Unable to fetch data from {url}. Status {response.status_code}")
            return None

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

        # To avoid being rate-limited by bbref
        time.sleep(4)
