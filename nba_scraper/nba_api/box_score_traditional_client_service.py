from nba_api.stats.endpoints import boxscoretraditionalv3
from nba_scraper.dto_models.player_stats_dto import PlayerStatsDto
from nba_scraper.dto_models.games_dto import GameDto
import pandas as pd
from datetime import date

class BoxScoreTraditionalClientService:

    def __init__(self):
        pass

    def _validated_aggregated_team_df(self, df: pd.DataFrame) -> pd.DataFrame: # <-- Should return DTO right away 
        if not df.shape[0] == 2:
            raise Exception("More than 2 rows found for aggregated box_scores")
        
        return df

    def fetch_team_aggregated_box_score_by_game_id(self, game_id: str) -> dict:
        raw_response = boxscoretraditionalv3.BoxScoreTraditionalV3(
            game_id=game_id
        )

        data_sets: list[pd.DataFrame] = raw_response.get_data_frames()

        # Third df in the dataset, ref. https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/boxscoretraditionalv3.md
        aggregated_box_score = self._validated_aggregated_team_df(data_sets[2])

        home_team: pd.Series = aggregated_box_score.iloc[0]
        away_team: pd.Series = aggregated_box_score.iloc[1]

        return {
            "game_id": home_team["gameId"],

            # This date has to be fetched from somwhere, possibly ScheduleLeaguev2 which has all the games and IDs
            "date": date.fromisoformat("1999-02-02"), 

            "home_team_id": int(home_team["teamId"]),
            "away_team_id": int(away_team["teamId"]),
            "home_score": int(home_team["points"]), 
            "away_score": int(away_team["points"]),
            "winner": int(home_team["teamId"]) if home_team["points"] > away_team["points"] else int(away_team["teamId"])
        }
    
    def _create_player_stats_dto(self, data_row: dict) -> PlayerStatsDto:
        return PlayerStatsDto(
            player_id = data_row["personId"],
            game_id=data_row["gameId"],
            team_id=data_row["teamId"],
            minutes=data_row["minutes"],
            field_goals_made=data_row["fieldGoalsMade"],
            field_goals_attempted=data_row["fieldGoalsAttempted"],
            field_goals_percentage=data_row["fieldGoalsPercentage"],
            three_pointers_made=data_row["threePointersMade"],
            three_pointers_attempted=data_row["threePointersAttempted"],
            three_pointers_percentage=data_row["threePointersPercentage"],
            free_throws_made=data_row["freeThrowsMade"],
            free_throws_attempted=data_row["freeThrowsAttempted"],
            free_throws_percentage=data_row["freeThrowsPercentage"],
            rebounds_offensive=data_row["reboundsOffensive"],
            rebounds_defensive=data_row["reboundsDefensive"],
            rebounds_total=data_row["reboundsTotal"],
            assists=data_row["assists"],
            steals=data_row["steals"],
            blocks=data_row["blocks"],
            turnovers=data_row["turnovers"],
            fouls_personal=data_row["foulsPersonal"],
            points=data_row["points"],
            plus_minus_points=data_row["plusMinusPoints"]
        )

    def fetch_player_box_score_by_game_id(self, game_id: str) -> list[PlayerStatsDto]:
        raw_response = boxscoretraditionalv3.BoxScoreTraditionalV3(
            game_id=game_id
        )

        data_sets: list[pd.DataFrame] = raw_response.get_data_frames()

        # Third df in the dataset, ref. https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/boxscoretraditionalv3.md
        # records make sure that we get list of records with their own key, 
        # instead of something like playerId: [123, 456] we get
        # [ {playerId: 123}, {playerId: 456}]
        player_box_scores = data_sets[0].to_dict("records") 

        # TODO Add validator, e.g. positions can only be C, F, G (PG, SF, PF?)

        player_stats_dto_list = [self._create_player_stats_dto(row) for row in player_box_scores]
        print(player_box_scores.head(1).T)

        


