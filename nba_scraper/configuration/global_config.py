DATA_FOLDER = "nba_scraper/data/"

SEASON_MONTHS = ["october", "november", "december",
                 "january", "february", "march", "april", "may", "june"]

CORONA_SEASON_MONTHS = {
    "2020": ["october", "november", "december",
             "january", "february", "march", "july", "august", "september"],
    "2021": ["december", "january", "february", "march", "july"]
}

MONTH_NAME_TO_NUMBER = {
    "JANUARY": "01",
    "FEBRUARY": "02",
    "MARCH": "03",
    "APRIL": "04",
    "MAY": "05",
    "JUNE": "06",
    "JULY": "07",
    "AUGUST": "08",
    "SEPTEMBER": "09",
    "OCTOBER": "10",
    "NOVEMBER": "11",
    "DECEMBER": "12"
}

MONTH_NUMBER_TO_MONTH_NAME = {
    "01": "JANUARY",
    "02": "FEBRUARY",
    "03": "MARCH",
    "04": "APRIL",
    "05": "MAY",
    "06": "JUNE",
    "07": "JULY",
    "08": "AUGUST",
    "09": "SEPTEMBER",
    "10": "OCTOBER",
    "11": "NOVEMBER",
    "12": "DECEMBER"
}

YEARS = ["2025", "2024", "2023", "2022", "2021", "2020"]

PLAYOFF_START = {
    "2024": "2024-04-20",
    "2023": "2023-04-15",
    "2022": "2022-04-16",
    "2021": "2021-05-22",
    "2020": "2020-08-17"
}

ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
            "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

ACTIVE_PLAYERS_FILE = "active_players.csv"
ACTIVE_PLAYERS_COLUMN_NAMES = ["active_player", "player_link"]

NBA_TEAMS = {
    "ATL":	"Atlanta Hawks",
    "BOS":	"Boston Celtics",
    "BRK":	"Brooklyn Nets",
    "CHO":	"Charlotte Hornets",
    "CHI":	"Chicago Bulls",
    "CLE":	"Cleveland Cavaliers",
    "DAL":	"Dallas Mavericks",
    "DEN":	"Denver Nuggets",
    "DET":	"Detroit Pistons",
    "GSW":	"Golden State Warriors",
    "HOU":	"Houston Rockets",
    "IND":	"Indiana Pacers",
    "LAC":	"Los Angeles Clippers",
    "LAL":	"Los Angeles Lakers",
    "MEM":	"Memphis Grizzlies",
    "MIA":	"Miami Heat",
    "MIL":	"Milwaukee Bucks",
    "MIN":	"Minnesota Timberwolves",
    "NOP":	"New Orleans Pelicans",
    "NYK":	"New York Knicks",
    "OKC":	"Oklahoma City Thunder",
    "ORL":	"Orlando Magic",
    "PHI":	"Philadelphia 76ers",
    "PHO":	"Phoenix Suns",
    "POR":	"Portland Trail Blazers",
    "SAC":	"Sacramento Kings",
    "SAS":	"San Antonio Spurs",
    "TOR":	"Toronto Raptors",
    "UTA":	"Utah Jazz",
    "WAS":	"Washington Wizards"
}

NBA_TEAM_FULL_NAME_TO_ABBRIV = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BRK",
    "Charlotte Hornets": "CHO",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHO",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS"
}
