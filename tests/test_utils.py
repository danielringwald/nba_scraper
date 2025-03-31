import unittest
import nba_scraper.configuration.global_config as gc
from nba_scraper.utils import Utils


SEASON_AND_MONTHS_OF_2025 = [("2024", "10"), ("2024", "11"), ("2024", "12"), ("2025", "01"), (
    "2025", "02"), ("2025", "03"), ("2025", "04"), ("2025", "05"), ("2025", "06")]


class TestUtils(unittest.TestCase):

    def test_choose_season_months(self):

        season_months = Utils.choose_season_months("2025")
        self.assertEqual(season_months, gc.SEASON_MONTHS)

        # Corona months
        season_months = Utils.choose_season_months("2020")
        self.assertEqual(season_months, gc.CORONA_SEASON_MONTHS["2020"])

        # Corona months
        season_months = Utils.choose_season_months("2021")
        self.assertEqual(season_months, gc.CORONA_SEASON_MONTHS["2021"])

    def test_get_year_and_months_of_season(self):

        season_months = Utils._get_year_and_months_of_season(2025)
        self.assertEquals(season_months, SEASON_AND_MONTHS_OF_2025)
