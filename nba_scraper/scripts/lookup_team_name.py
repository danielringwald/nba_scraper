import argparse
import logging
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.dao.repository.team_name_repository import TeamNameRepository
from nba_scraper.configuration.logging_config import init_logging
init_logging()

logger = logging.getLogger(__name__)

season_games_repo = SeasonGamesRepository()
team_name_repo = TeamNameRepository()


def lookup_team_name(team_name: str) -> None:
    team_id = team_name_repo.get_team_information(team_id=team_name)

    logger.info("Team name %s has team_id: %s", team_name, team_id)


if __name__ == "__main__":
    # Example usage
    parser = argparse.ArgumentParser(description="NBA scraper script")
    parser.add_argument("team_name", help="NBA team name to lookup")

    args = parser.parse_args()

    lookup_team_name(args.team_name)
