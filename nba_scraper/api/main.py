from fastapi import FastAPI, HTTPException
from nba_scraper.dao.repository.box_score_traditional_repository import BoxScoreTraditionalRepository

app = FastAPI(title="NBA Stats API", version="0.1")

# Service / repository instance
box_score_repo = BoxScoreTraditionalRepository()


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
