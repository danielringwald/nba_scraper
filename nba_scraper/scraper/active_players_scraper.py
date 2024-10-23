from ..configuration.global_config import ALPHABET, SEASON_MONTHS, DATA_FOLDER
from bs4 import BeautifulSoup
from .common_scraper import CommonScarper
import time
import pandas as pd


class ActivePlayersScraper:

    def __init__(self, base_url):
        self.base_url = base_url

    def parse_statistics(self, html_content):
        """Parses the HTML content and extracts the relevant data."""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the table (this example assumes the stats are in a table)
        table = soup.find("div", {"id": "div_players"})

        # Extract table headers
        headers = [th.text for th in table.find('thead').find_all('th')]

        player_names = []
        for player_object in table.find_all('strong'):

            player_a_tag = player_object.find('a')

            player_link = player_a_tag.get('href')

            player_name = player_object.get_text()

            player_names.append([player_name, player_link])

        print(
            f"Parsed URL. Found {str(len(player_names))} active players.")

        return pd.DataFrame(player_names, columns=['active_players', 'link'])


if __name__ == "__main__":
    # Example usage
    base_url = "https://www.basketball-reference.com"

    scraper = ActivePlayersScraper(base_url)

    file_name = "active_players.csv"

    active_players_list = []
    for letter in ALPHABET:
        output_file = DATA_FOLDER + file_name

        endpoint = "players/" + str.lower(letter)

        print(f"Scarping endpoint {endpoint}")
        active_players_list.append(CommonScarper.scrape_nba_stats_df(
            endpoint, parse_statistics_method=scraper.parse_statistics))

        # To avoid being rate-limited
        time.sleep(4)

    active_players_df = pd.concat(active_players_list)

    CommonScarper.save_to_csv(
        active_players_df, filename=DATA_FOLDER + file_name)
