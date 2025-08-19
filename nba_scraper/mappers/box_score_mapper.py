import pandas as pd
from nba_scraper.models.game_box_score import GameBoxScore
from nba_scraper.models.box_score_row import BoxScoreRow


class BoxScoreMapper():

    @staticmethod
    def map_df_to_box_score_game(item_id: str, df: pd.DataFrame) -> GameBoxScore:

        def to_int(val) -> int:
            # Helper: convert to int safely, treating NaN and None as 0
            try:
                return int(val)
            except (ValueError, TypeError):
                return 0

        def to_float(val) -> float:
            # Helper: convert to int safely, treating NaN and None as 0
            try:
                return float(val)
            except (ValueError, TypeError):
                return float(0)

        player_scores: list[BoxScoreRow] = []

        for idx, (_, row) in enumerate(df.iterrows()):
            # Map each row to BoxScoreRow
            player_score = BoxScoreRow(
                IS_STARTER=(idx < 5),

                PLAYER_NAME=row.get('Starters') or row.get(
                    'PLAYER_NAME') or "Unknown",
                MP=str(row.get('MP', '0')),
                FG=to_int(row.get('FG')),
                FGA=to_int(row.get('FGA')),
                FG_PERCENTAGE=to_float(row.get('FG%')) if pd.notnull(
                    row.get('FG%')) else 0,
                THREE_POINTERS_MADE=to_int(row.get('3P')),
                THREE_POINTERS_ATTEMPTED=to_int(row.get('3PA')),
                THREE_POINTERS_PERCENTAGE=to_float(
                    row.get('3P%')) if pd.notnull(row.get('3P%')) else 0,
                FT=to_int(row.get('FT')),
                FTA=to_int(row.get('FTA')),
                FT_PERCENTAGE=to_float(row.get('FT%')) if pd.notnull(
                    row.get('FT%')) else 0,
                ORB=to_int(row.get('ORB')),
                DRB=to_int(row.get('DRB')),
                TRB=to_int(row.get('TRB')),
                AST=to_int(row.get('AST')),
                STL=to_int(row.get('STL')),
                BLK=to_int(row.get('BLK')),
                TOV=to_int(row.get('TOV')),
                PF=to_int(row.get('PF')),
                PTS=to_int(row.get('PTS')),
                GAME_SCORE=to_float(row.get('GmSc')) if pd.notnull(
                    row.get('GmSc')) else 0,
                PLUS_MINUS=to_int(row.get('+/-'))
            )
            player_scores.append(player_score)

        return GameBoxScore(
            id=item_id,
            home_team=None,
            away_team=None,
            home_team_score=None,
            away_team_score=None,
            player_scores=player_scores
        )
