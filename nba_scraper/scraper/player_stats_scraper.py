from bs4 import BeautifulSoup
import pandas as pd
from ..configuration.global_config import DATA_FOLDER, ACTIVE_PLAYERS_FILE
from ..configuration.player_stats import DATA_DIRECTORY_PATH
import time
from .common_scraper import CommonScarper
from ..utils import Utils
import logging


class PlayerStatsScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def parse_statistics(self, html_content):
        """Parses the HTML content and extracts the relevant data."""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the table (this example assumes the stats are in a table)
        table = soup.find("div", {"id": "div_per_game"})
        if table is None:
            table = soup.find("div", {"id": "div_per_game_stats"})

        if table is None:
            raise Exception("Can't parse the div")

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

    if not Utils.is_file_in_directory(ACTIVE_PLAYERS_FILE, DATA_FOLDER):
        print(
            "Active players file doesn't exist. Raising exception")
        raise FileNotFoundError(f"{ACTIVE_PLAYERS_FILE} not found.")

    active_players = pd.read_csv(DATA_FOLDER + ACTIVE_PLAYERS_FILE)

    for player_row in active_players.itertuples():

        # The first value will be the DataFrame index
        player_name = player_row[1]
        player_endpoint = player_row[2]

        endpoint = player_endpoint

        player_file_ending = str(
            player_name).lower().replace(" ", "_") + ".csv"
        output_file = DATA_DIRECTORY_PATH + player_file_ending

        if Utils.is_file_in_directory(player_file_ending, DATA_DIRECTORY_PATH):
            print(
                f"Player stats file {output_file} already exist. Continuing...")
            continue

        CommonScarper.scrape_nba_stats(
            endpoint, output_file, parse_statistics_method=scraper.parse_statistics)

        # To avoid being rate-limited
        time.sleep(4)
