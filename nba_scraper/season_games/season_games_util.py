from nba_scraper.utils import Utils


class SeasonGamesUtil:

    @staticmethod
    def append_winner_column(season_games: dict[str, str] | list[dict[str, str]], team_id: str = None) -> list[dict[str, str]]:
        """
            Append a 'winner' column to the season games data, indicating the winning team_id

            If team_id is provided, the 'winner' column will be 1 if the specified team won, else 0
            If team_id is NOT provided, the 'winner' column will contain the winning team_id
        """

        season_games = Utils.to_list(season_games)

        if team_id:
            for game in season_games:
                home_score = game["home_team_score"]
                away_score = game["away_team_score"]

                if home_score > away_score:
                    if game["home_team_id"] == team_id:
                        game['winner'] = 1
                    else:
                        game['winner'] = 0
                else:
                    if game["away_team_id"] == team_id:
                        game['winner'] = 1
                    else:
                        game['winner'] = 0
            return season_games

        for game in season_games:
            if game["home_team_score"] > game["away_team_score"]:
                game["winner"] = game["home_team_id"]
            else:
                game["winner"] = game["away_team_id"]
        return season_games
