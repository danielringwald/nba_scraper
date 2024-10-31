import nba_scraper.configuration.schedule_and_results as sar


class HeaderCreator:

    @staticmethod
    def create_schedule_and_results_header():
        header = []

        header.append(sar.DATE)
        header.append(sar.START_TIME)
        header.append(sar.AWAY_TEAM)
        header.append(sar.AWAY_TEAM_POINTS)
        header.append(sar.HOME_TEAM)
        header.append(sar.HOME_TEAM_POINTS)
        header.append(sar.BOX_SCORE_LINK)
        header.append(sar.OVER_TIME)
        header.append(sar.ATTENDANCE)
        header.append(sar.LENGTH_OF_GAME)
        header.append(sar.ARENA)
        header.append(sar.NOTES)

        return header
