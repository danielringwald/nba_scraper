from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import scheduleleaguev2
"""
    COMMENT

    gameStatus: Observation, finished games have gameStatus=3, not started games have gameStatus=1. 
    Guess is that games in progress have gameStatus=2
"""
from nba_api.stats.endpoints import boxscoretraditionalv3
from nba_api.stats.library.parameters import LeagueID
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository

# data = shotchartdetail.ShotChartDetail(
#     player_id = 201939,
#     team_id = '1610612744',
#     season_type_all_star = 'Regular Season',
#     season_nullable = '2023-24',
#     context_measure_simple = 'FGA')

# pandas data frames (optional: pip install pandas)
# print(data.get_data_frames()[0].to_string())

# data = scheduleleaguev2.ScheduleLeagueV2(season="2023-24")
#
# print("size", data.get_data_frames()[0].shape)

# data.get_data_frames()[0].iloc[0:100].apply(
#     lambda row: print(row.to_string()), axis=1)

# data = boxscoretraditionalv3.BoxScoreTraditionalV3(
#     game_id='0022400061'
# )
# data.get_data_frames()[0].apply(
#     lambda row: print(row.to_string() + "\n"), axis=1)

# from nba_api.stats.library.data import teams
#
# for team in teams:
#     print(team)

# sgr = SeasonGamesRepository()
#
# print(sgr.get_season_games("2024-25"))

from nba_scraper.dao.repository.box_score_traditional_repository import BoxScoreTraditionalRepository
data = BoxScoreTraditionalRepository(
).fetch_box_score_from_team_and_season("1610612757", "2024-25")
print(data)
# print(BoxScoreTraditionalRepository().database_select_all())

# game_ids = [game_id for (game_id, *_) in data]
# game_ids = set(game_ids)
# print(game_ids)
