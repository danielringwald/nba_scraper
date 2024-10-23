from bs4 import BeautifulSoup
import pandas as pd
from ..configuration.global_config import SEASON_MONTHS, YEARS, DATA_FOLDER
from ..configuration.schedule_and_results import DIRECTORY_PATH
import time
from .common_scraper import CommonScarper
from ..utils import Utils
import logging

CURRENT_DATA_FOLDER = DATA_FOLDER + DIRECTORY_PATH


class PlayerStatsScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def parse_statistics(self, html_content):
        """Parses the HTML content and extracts the relevant data."""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the table (this example assumes the stats are in a table)
        table = soup.find("div", {"id": "div_schedule"})

        # Extract table headers
        headers = [th.text for th in table.find('thead').find_all('th')]

        # Extract table rows
        body_headers = []
        rows = []
        for tr in table.find('tbody').find_all('th'):
            row = [a.text for a in tr.find_all('a')]
            body_headers.append(row)
        for i, tr in enumerate(table.find('tbody').find_all('tr')):
            row = [td.text for td in tr.find_all('td')]
            rows.append(row)

        body_rows = []
        for i in range(len(body_headers)):
            body_rows.append(body_headers[i] + rows[i])

        # Convert to a pandas DataFrame
        df = pd.DataFrame(body_rows, columns=headers)
        return df


if __name__ == "__main__":
    # Example usage
    base_url = "https://www.basketball-reference.com"

    scraper = PlayerStatsScraper(base_url)
    for year in YEARS:
        for month in SEASON_MONTHS:
            file_name = year + "_" + month + "_games_result.csv"
            output_file = CURRENT_DATA_FOLDER + file_name

            if Utils.is_file_in_directory(file_name, CURRENT_DATA_FOLDER):
                logging.info(
                    "File {} already exists. Continuing...".format(file_name))
                continue

            endpoint = "leagues/NBA_" + year + "_games-" + month + ".html"

            CommonScarper.scrape_nba_stats(
                endpoint, output_file, parse_statistics_method=scraper.parse_statistics)

            # To avoid being rate-limited
            time.sleep(5)
