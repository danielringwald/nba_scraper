import unittest
from nba_scraper.nba_api.teams_client_service import TeamClientService, NBA_TEAMS
from nba_scraper.dto_models.teams_dto import TeamDto

class TestTeamDto(unittest.TestCase):
    def test_from_api_list(self):
        sample = [10, "LAL", None, None, "Los Angeles", "Lakers"]
        dto = TeamDto.from_api_list(sample)
        self.assertEqual(dto.team_id, 10)
        self.assertEqual(dto.team_abbreviation, "LAL")
        self.assertEqual(dto.city, "Los Angeles")
        self.assertEqual(dto.name, "Lakers")

class TestTeamClientService(unittest.TestCase):
    def setUp(self):
        # Patch NBA_TEAMS with a controlled dataset
        self.original_teams = NBA_TEAMS
        self.mock_teams = [
            [1, "ATL", None, None, "Atlanta", "Hawks"],
            [2, "BOS", None, None, "Boston", "Celtics"],
        ]
        NBA_TEAMS[:] = self.mock_teams
        self.service = TeamClientService()

    def tearDown(self):
        # Restore original NBA_TEAMS
        NBA_TEAMS[:] = self.original_teams

    def test_fetch_all_teams_returns_expected_set(self):
        result = self.service.fetch_all_teams()
        expected = {
            (1, "ATL", "Atlanta", "Hawks"),
            (2, "BOS", "Boston", "Celtics"),
        }
        self.assertEqual(set((t.team_id, t.team_abbreviation, t.city, t.name) for t in result), expected)
        self.assertIsInstance(result, set)
        self.assertEqual(len(result), 2)

if __name__ == "__main__":
    unittest.main()
