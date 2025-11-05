import argparse
import pandas as pd
from nba_scraper.dao.repository.box_score_traditional_repository import BoxScoreTraditionalRepository
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.dao.repository.team_name_repository import TeamNameRepository

box_score_trad_repo = BoxScoreTraditionalRepository()
season_games_repo = SeasonGamesRepository()
team_name_repo = TeamNameRepository()


def redirect_to_game_website(game_id: str) -> None:
    import webbrowser

    base_url = "https://www.nba.com/game/"

    game = season_games_repo.get_single_game(game_id=game_id)
    if not game:
        print(f"No game found with game_id: {game_id}")
        return
    columns = season_games_repo.get_table_columns()

    games_df = pd.DataFrame([game], columns=columns).iloc[0]

    game_url_part = f'{games_df["away_team_abbreviation"]}-{games_df["home_team_abbreviation"]}-{games_df["game_id"]}'

    full_url = f"{base_url}{game_url_part}"

    webbrowser.open(full_url)


if __name__ == "__main__":
    # Example usage
    parser = argparse.ArgumentParser(description="NBA scraper script")
    parser.add_argument("game_id", help="NBA game ID to scrape")

    args = parser.parse_args()

    redirect_to_game_website(args.game_id)
