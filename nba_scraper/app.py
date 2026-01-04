import logging
import sys
import os
import argparse
from nba_scraper.index import app


def setup_logging():
    parser = argparse.ArgumentParser(description="NBA Scraper Dashboard")
    parser.add_argument('--log-level',
                        choices=["debug", "info",
                                 "warning", "error", "critical"],
                        help="Set the logging level",
                        default="warning")  # Set default to warning since that is Python standard
    args = parser.parse_args()

    if args.log_level:
        log_level = getattr(logging, args.log_level.upper(), None)
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )

        print(
            f"Logging level set to {args.log_level.upper()}. Use --log-level to change it.")


if __name__ == "__main__":
    setup_logging()

    logging.info("Starting NBA Scraper Dashboard")
    app.run(debug=True)
    