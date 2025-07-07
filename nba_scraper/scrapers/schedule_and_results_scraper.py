from bs4 import BeautifulSoup
import pandas as pd
from ..configuration.global_config import SEASON_MONTHS, YEARS, CORONA_SEASON_MONTHS
from ..configuration.schedule_and_results import DIRECTORY_PATH
from .common_scraper import CommonScarper
from ..utils import Utils

CURRENT_DATA_FOLDER = DIRECTORY_PATH


class ScheduleAndResultsScraper:
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


def _choose_season_months(year):
    """
        Function to choose which months to scrape. This is because of corona season where the season was irregular.
    """
    if year == "2020" or year == "2021":
        return CORONA_SEASON_MONTHS[year]
    return SEASON_MONTHS


if __name__ == "__main__":
    # Example usage
    base_url = "https://www.basketball-reference.com"

    scraper = ScheduleAndResultsScraper(base_url)
    for year in YEARS:
        for month in _choose_season_months(year):
            file_name = year + "_" + month + "_games_result.csv"

            endpoint = "leagues/NBA_" + year + "_games-" + month + ".html"

            output_file = CURRENT_DATA_FOLDER + file_name

            if Utils.is_file_in_directory(file_name, CURRENT_DATA_FOLDER):
                print(
                    "File {} already exists. Continuing...".format(file_name))
                continue

            CommonScarper.scrape_and_save_data(scraper, endpoint, output_file)
