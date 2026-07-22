from nba_api.stats.endpoints import boxscoretraditionalv3
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import boxscoreplayertrackv3
from nba_scraper.nba_api.box_score_traditional_client_service import BoxScoreTraditionalClientService

import pandas as pd

def main():
    game_data = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id="0022500893")

    # player_info = commonplayerinfo.CommonPlayerInfo(player_id="76001")
    # print("Player info")
    # print(player_info.get_data_frames()[0])
    # 
    # player_box_score = boxscoreplayertrackv3.BoxScorePlayerTrackV3(game_id="0022500893")
    # print("Player box score")
    # print(player_box_score.get_data_frames()[0].iloc[3])
     
    BoxScoreTraditionalClientService().fetch_player_box_score_by_game_id("0022500893")


if __name__ == "__main__":
    main()
