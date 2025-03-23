from .global_config import DATA_FOLDER

DIRECTORY_PATH = DATA_FOLDER + "box_score/"

TOTAL_BOX_SCORES_PATH = DIRECTORY_PATH + "total_box_scores/"

# start with yyyymmdd then awayTeam_homeTeam, e.g. 20190202TOR_LAL
BOX_SCORE_DATA_FILE_TEMPLATE = "{}{}"

PLAYER = "Starters"
MP = "MP"
FG = "FG"
FGA = "FGA"
FG_PERCENTAGE = "FG%"
THREE_POINTERS_MADE = "3P"
THREE_POINTERS_ATTEMPTED = "3PA"
THREE_POINTERS_PERCENTAGE = "3P%"
FT = "FT"
FTA = "FTA"
FT_PERCENTAGE = "FT%"
ORB = "ORB"
DRB = "DRB"
TRB = "TRB"
AST = "AST"
STL = "STL"
BLK = "BLK"
TOV = "TOV"
PF = "PF"
PTS = "PTS"
GAME_SCORE = "GmSc"
PLUS_MINUS = "+/-"
