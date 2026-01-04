import pandas as pd
from nba_scraper.configuration.database_config import SeasonGamesColumn as sgc
from nba_scraper.mlops.pipeline.config import PointDiffFeatures as pdf

class PointDiffHelper:

    @staticmethod
    def _build_team_game_history(df: pd.DataFrame) -> pd.DataFrame:
        records = []

        for _, row in df.iterrows():
            # Home team
            records.append({
                pdf.GAME_ID: row[sgc.GAME_ID],
                pdf.DATE: row[sgc.DATE],
                pdf.TEAM_ABBREVIATION: row[sgc.HOME_TEAM_ABBREVIATION],
                pdf.IS_HOME: 1,
                pdf.POINTS_SCORED: row[sgc.HOME_TEAM_SCORE],
                pdf.POINTS_ALLOWED: row[sgc.AWAY_TEAM_SCORE],
            })

            # Away team
            records.append({
                pdf.GAME_ID: row[sgc.GAME_ID],
                pdf.DATE: row[sgc.DATE],
                pdf.TEAM_ABBREVIATION: row[sgc.AWAY_TEAM_ABBREVIATION],
                pdf.IS_HOME: 0,
                pdf.POINTS_SCORED: row[sgc.AWAY_TEAM_SCORE],
                pdf.POINTS_ALLOWED: row[sgc.HOME_TEAM_SCORE],
            })

        team_df = pd.DataFrame(records)
        team_df[pdf.POINT_DIFF] = (
            team_df[pdf.POINTS_SCORED] - team_df[pdf.POINTS_ALLOWED]
        )

        return team_df.sort_values([pdf.TEAM_ABBREVIATION, pdf.DATE])
    
    @staticmethod
    def _add_rolling_features(team_df: pd.DataFrame, n_games: int) -> pd.DataFrame:
        team_df = team_df.copy()

        team_df[pdf.AVG_POINT_DIFF_LAST_N] = (
            team_df
            .groupby(pdf.TEAM_ABBREVIATION)[pdf.POINT_DIFF]
            .shift(1)
            .rolling(n_games)
            .mean()
        )

        team_df[pdf.AVG_POINTS_SCORED_LAST_N] = (
            team_df
            .groupby(pdf.TEAM_ABBREVIATION)[pdf.POINTS_SCORED]
            .shift(1)
            .rolling(n_games)
            .mean()
        )

        team_df[pdf.AVG_POINTS_ALLOWED_LAST_N] = (
            team_df
            .groupby(pdf.TEAM_ABBREVIATION)[pdf.POINT_DIFF]
            .shift(1)
            .rolling(n_games)
            .mean()
        )

        team_df[pdf.DAYS_SINCE_LAST_GAME] = (
            team_df
            .groupby(pdf.TEAM_ABBREVIATION)[pdf.DATE]
            .diff()
            .dt.days
        )

        team_df[pdf.IS_BACK_TO_BACK] = (team_df[pdf.DAYS_SINCE_LAST_GAME] <= 1).astype(int)

        return team_df
