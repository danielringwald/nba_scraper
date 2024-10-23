import requests


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
    def save_to_csv(df, filename):
        """Saves the DataFrame to a CSV file."""
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    @staticmethod
    def scrape_nba_stats(endpoint, output_file, parse_statistics_method):
        """Main function to scrape stats and save to CSV."""
        html_content = CommonScarper.fetch_page(endpoint)
        if html_content:
            stats_df = parse_statistics_method(html_content)
            CommonScarper.save_to_csv(stats_df, output_file)

    @staticmethod
    def scrape_nba_stats_df(endpoint, parse_statistics_method):
        """Main function to scrape stats and save to CSV."""
        html_content = CommonScarper.fetch_page(endpoint)
        if html_content:
            return parse_statistics_method(html_content)
