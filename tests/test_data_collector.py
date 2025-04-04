import unittest
import xarray as xr
import nba_scraper.data_collector as dc

class TestDataCollector(unittest.TestCase):

    def test_get_box_scores_by_team_and_season(self):

        box_scores = dc.get_box_scores_by_team_and_season("ATL", 2024)
        print(box_scores)
        self.assertEquals(box_scores, xr.DataArray())

if __name__ == "__main__":
    unittest.main()
