# Path to database file (DuckDB)
DATABASE_PATH = "nba_scraper.db"

# --- Table Name Constants ---
TEAM_NAME_INFORMATION_TABLE_NAME = "teams_information"
BOX_SCORE_TRADITIONAL_TABLE_NAME = "box_score_traditional"
SEASON_GAMES_TABLE_NAME = "season_games"


class SeasonGamesColumn:
    """Constants for the 'season_games' table columns."""
    GAME_ID = 'game_id'
    SEASON = 'season'
    DATE = 'date'
    GAME_STATUS = 'game_status'
    GAME_LABEL = 'game_label'

    # Home Team Fields
    HOME_TEAM_ID = 'home_team_id'
    HOME_TEAM_ABBREVIATION = 'home_team_abbreviation'
    HOME_TEAM_SCORE = 'home_team_score'

    # Away Team Fields
    AWAY_TEAM_ID = 'away_team_id'
    AWAY_TEAM_ABBREVIATION = 'away_team_abbreviation'
    AWAY_TEAM_SCORE = 'away_team_score'

    ALL_COLUMNS = [
        GAME_ID, SEASON, DATE, GAME_STATUS, GAME_LABEL,
        HOME_TEAM_ID, HOME_TEAM_ABBREVIATION, HOME_TEAM_SCORE,
        AWAY_TEAM_ID, AWAY_TEAM_ABBREVIATION, AWAY_TEAM_SCORE
    ]


class TeamInformationColumn:
    """Constants for the 'teams_information' table columns."""
    TEAM_ID = 'team_id'
    TEAM_ABBREVIATION = 'team_abbreviation'
    TEAM_NAME = 'team_name'

    ALL_COLUMNS = [
        TEAM_ID, TEAM_ABBREVIATION, TEAM_NAME
    ]


class BoxScoreTraditionalColumn:
    """
    Constants for the 'box_score_traditional' table columns 
    (from your previous prompt).
    """
    # Identifiers
    GAME_ID = 'game_id'
    SEASON = 'season'
    TEAM_ID = 'team_id'
    PLAYER_ID = 'player_id'
    PLAYER_NAME = 'player_name'

    # Core Stats
    STARTER = 'starter'
    SECONDS_PLAYED = 'seconds_played'
    ASSISTS = 'assists'
    STEALS = 'steals'
    BLOCKS = 'blocks'
    TURNOVERS = 'turnovers'
    PERSONAL_FOULS = 'personal_fouls'
    POINTS = 'points'
    PLUS_MINUS_POINTS = 'plus_minus_points'

    # Shooting Stats
    FIELD_GOALS_MADE = 'field_goals_made'
    FIELD_GOALS_ATTEMPTED = 'field_goals_attempted'
    FIELD_GOALS_PERCENTAGE = 'field_goals_percentage'
    THREE_POINTERS_MADE = 'three_pointers_made'
    THREE_POINTERS_ATTEMPTED = 'three_pointers_attempted'
    THREE_POINTERS_PERCENTAGE = 'three_pointers_percentage'
    FREE_THROWS_MADE = 'free_throws_made'
    FREE_THROWS_ATTEMPTED = 'free_throws_attempted'
    FREE_THROWS_PERCENTAGE = 'free_throws_percentage'

    # Rebounds
    OFFENSIVE_REBOUNDS = 'offensive_rebounds'
    DEFENSIVE_REBOUNDS = 'defensive_rebounds'
    TOTAL_REBOUNDS = 'total_rebounds'

    ALL_COLUMNS = [
        GAME_ID, SEASON, TEAM_ID, PLAYER_ID, PLAYER_NAME, STARTER,
        SECONDS_PLAYED, FIELD_GOALS_MADE, FIELD_GOALS_ATTEMPTED,
        FIELD_GOALS_PERCENTAGE, THREE_POINTERS_MADE,
        THREE_POINTERS_ATTEMPTED, THREE_POINTERS_PERCENTAGE,
        FREE_THROWS_MADE, FREE_THROWS_ATTEMPTED, FREE_THROWS_PERCENTAGE,
        OFFENSIVE_REBOUNDS, DEFENSIVE_REBOUNDS, TOTAL_REBOUNDS,
        ASSISTS, STEALS, BLOCKS, TURNOVERS, PERSONAL_FOULS, POINTS,
        PLUS_MINUS_POINTS
    ]
