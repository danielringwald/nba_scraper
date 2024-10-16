import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import SEASON_MONTHS, YEARS
import time

class NBAScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_page(self, endpoint):
        """Fetches the HTML content of the page."""
        url = f"https://www.basketball-reference.com/{endpoint}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: Unable to fetch data from {url}")
            return None

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

    def save_to_csv(self, df, filename):
        """Saves the DataFrame to a CSV file."""
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def scrape_nba_stats(self, endpoint, output_file):
        """Main function to scrape stats and save to CSV."""
        html_content = self.fetch_page(endpoint)
        if html_content:
            stats_df = self.parse_statistics(html_content)
            self.save_to_csv(stats_df, output_file)

if __name__ == "__main__":
    # Example usage
    base_url = "https://www.basketball-reference.com"

    scraper = NBAScraper(base_url)
    for year in YEARS:
        for month in SEASON_MONTHS:
            endpoint = "leagues/NBA_" + year + "_games-" + month + ".html"
            output_file = "monthly_scores/" + year + "_" + month + "_games_result.csv"
            scraper.scrape_nba_stats(endpoint, output_file)
            
            # To avoid being rate-limited
            time.sleep(5)
