from nba_scraper.configuration.logging_config import init_logging
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.dao.repository.box_score_traditional_repository import BoxScoreTraditionalRepository
from fastapi import FastAPI, HTTPException, Query
import logging

init_logging()

logger = logging.getLogger(__name__)
logger.info("Starting NBA Scraper API")

app = FastAPI(title="NBA Stats API", version="0.1")

# Service / repository instance
box_score_repo = BoxScoreTraditionalRepository()
season_games_repo = SeasonGamesRepository()


# REST endpoint equivalent to Spring @GetMapping("/boxscore")
@app.get("/boxscore")
def get_box_score(team_id: str, season: str = None):
    """
    Get box scores by team and season
    """
    try:
        results = box_score_repo.fetch_box_score_by_team_and_season(
            team_id=team_id, season=season)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


# Another endpoint example
@app.get("/boxscore/season/{season}")
def get_all_box_scores_from_season(season: str):
    try:
        results = box_score_repo.fetch_all_box_scores_from_season(
            season=season)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/season/games/latest/")
def get_n_latest_box_scores_by_team(team_id: str, annotate_winner: bool = Query(True), limit: int = 5):
    try:
        results = season_games_repo.get_games_by_team(
            team_id=team_id, limit=limit)

        if annotate_winner:
            for game in results:
                home_score = game['home_team_score']
                away_score = game['away_team_score']
                if home_score > away_score:
                    game['winner'] = game['home_team_abbreviation']
                elif away_score > home_score:
                    game['winner'] = game['away_team_abbreviation']
                else:
                    game['winner'] = 'Tie'

        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
