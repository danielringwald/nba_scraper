from bs4 import BeautifulSoup, Comment, Tag
import pandas as pd
import os
import time
from nba_scraper.configuration.global_config import YEARS
from nba_scraper.configuration.box_score import DIRECTORY_PATH, BOX_SCORE_YEARS_PARSED
from nba_scraper.scrapers.common_scraper import CommonScarper
from nba_scraper.utils import Utils

CURRENT_DATA_FOLDER = DIRECTORY_PATH


class BoxScoreScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def parse_statistics(self, html_content):
        """Parses the HTML content and extracts the relevant data."""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the table (this example assumes the stats are in a table)
        table = soup.find("div", {"id": "div_schedule"})

        # Extract table rows
        body_headers = []
        for tr in table.find('tbody').find_all('th'):
            row = [a.text for a in tr.find_all('a')]
            body_headers.append(row)
        for i, tr in enumerate(table.find('tbody').find_all('tr')):
            row = [td for td in tr.find_all('td')
                   if td.text == "Box Score"]
            for box_score in row:
                box_score_link = box_score.find("a", href=True)["href"]

                self.parse_child_page(box_score_link)

    def parse_child_page(self, endpoint: str):
        # Collect the game ID
        game_id = endpoint.split("/")[-1].split(".")[0]
        if any(game_id in box_score for box_score in os.listdir(CURRENT_DATA_FOLDER + "total_box_scores")):
            print("Game with id {} already parsed.".format(game_id))
            return

        html_content = CommonScarper.fetch_page(endpoint)

        soup = BeautifulSoup(html_content, 'html.parser')

        try:
            line_score_df = self._parse_line_score(soup)
            four_factors_df = self._parse_four_factor(soup)

            CommonScarper.save_to_csv(
                line_score_df, CURRENT_DATA_FOLDER + "line_score/" + game_id + ".csv")
            CommonScarper.save_to_csv(
                four_factors_df, CURRENT_DATA_FOLDER + "four_factors/" + game_id + ".csv")

            AWAY_TEAM = str(line_score_df.iloc[0, 0])
            HOME_TEAM = str(line_score_df.iloc[1, 0])

            total_box_score_away = self._parse_box_score_stats(
                soup, "div_box-" + AWAY_TEAM + "-game-basic")
            output_file = CURRENT_DATA_FOLDER + "total_box_scores/" + \
                game_id + "_" + AWAY_TEAM + ".csv"
            CommonScarper.save_to_csv(
                total_box_score_away, output_file)

            total_box_score_home = self._parse_box_score_stats(
                soup, "div_box-" + HOME_TEAM + "-game-basic")
            output_file = CURRENT_DATA_FOLDER + "total_box_scores/" + \
                game_id + "_" + HOME_TEAM + ".csv"
            CommonScarper.save_to_csv(
                total_box_score_home, output_file)

            for team in [AWAY_TEAM, HOME_TEAM]:
                for quarter in range(1, 5):
                    div_id = "div_box-" + team + "-q" + str(quarter) + "-basic"
                    output_file = CURRENT_DATA_FOLDER + "q" + \
                        str(quarter) + "/" + game_id + "_" + team + ".csv"

                    quarter_box_score = self._parse_box_score_stats(
                        soup, div_id)

                    CommonScarper.save_to_csv(
                        quarter_box_score, output_file)
        except Exception as e:
            print("Game raised exception", game_id)
            raise Exception(e)

        time.sleep(4)

    def _parse_box_score_stats(self, soup: BeautifulSoup, div_id):
        return self._get_headers_and_body_from_table(soup.find("div", {"id": div_id}))

    def _parse_line_score(self, soup: BeautifulSoup) -> pd.DataFrame:
        # table = soup.find("div", {"id": "div_line_score"})
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            # Search for a specific div inside the comment
            if "div_line_score" in comment:
                comment_soup = BeautifulSoup(comment, "html.parser")
                table = comment_soup.find("div", {"id": "div_line_score"})

        return self._get_headers_and_body_from_table(table)

    def _parse_four_factor(self, soup: BeautifulSoup) -> pd.DataFrame:
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            # Search for a specific div inside the comment
            if "div_four_factors" in comment:
                comment_soup = BeautifulSoup(comment, "html.parser")
                table = comment_soup.find("div", {"id": "div_four_factors"})

        return self._get_headers_and_body_from_table(table)

    def _get_headers_and_body_from_table(self, table: Tag) -> pd.DataFrame:

        headers = [th.text for th in table.find('thead').find_all('th')
                   if ("over_header" not in th.get("class", []) and th.text != "")]

        body_headers = []
        rows = []
        for tr in table.find('tbody').find_all('th'):
            row = [a.text for a in tr.find_all('a')]

            # To make sure that headers in the middle of the table don't affect
            if row != []:
                body_headers.append(row)
        for i, tr in enumerate(table.find('tbody').find_all('tr')):
            if "thead" not in tr.get("class", []):
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

    scraper = BoxScoreScraper(base_url)

    for year in [y for y in YEARS if y not in BOX_SCORE_YEARS_PARSED]:
        for month in Utils.choose_season_months(year):
            endpoint = "leagues/NBA_" + year + "_games-" + month + ".html"

            CommonScarper.scrape_and_save_data(scraper, endpoint, None, False)

    print("Parsing completed")
