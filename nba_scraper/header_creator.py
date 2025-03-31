import nba_scraper.configuration.schedule_and_results as sar
import nba_scraper.configuration.box_score as bs


class HeaderCreator:

    @staticmethod
    def create_schedule_and_results_headers():
        headers = []

        headers.append(sar.DATE)
        headers.append(sar.START_TIME)
        headers.append(sar.AWAY_TEAM)
        headers.append(sar.AWAY_TEAM_POINTS)
        headers.append(sar.HOME_TEAM)
        headers.append(sar.HOME_TEAM_POINTS)
        headers.append(sar.BOX_SCORE_LINK)
        headers.append(sar.OVER_TIME)
        headers.append(sar.ATTENDANCE)
        headers.append(sar.LENGTH_OF_GAME)
        headers.append(sar.ARENA)
        headers.append(sar.NOTES)

        return headers

    @staticmethod
    def create_box_score_total_score_headers():
        headers = []

        headers.append(bs.PLAYER)
        headers.append(bs.MP)
        headers.append(bs.FG)
        headers.append(bs.FGA)
        headers.append(bs.FG_PERCENTAGE)
        headers.append(bs.THREE_POINTERS_MADE)
        headers.append(bs.THREE_POINTERS_ATTEMPTED)
        headers.append(bs.THREE_POINTERS_PERCENTAGE)
        headers.append(bs.FT)
        headers.append(bs.FTA)
        headers.append(bs.FT_PERCENTAGE)
        headers.append(bs.ORB)
        headers.append(bs.DRB)
        headers.append(bs.TRB)
        headers.append(bs.AST)
        headers.append(bs.STL)
        headers.append(bs.BLK)
        headers.append(bs.TOV)
        headers.append(bs.PF)
        headers.append(bs.PTS)
        headers.append(bs.GAME_SCORE)
        headers.append(bs.PLUS_MINUS)

        return headers
