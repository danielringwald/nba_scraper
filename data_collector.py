import os
import pandas as pd
import matplotlib.pyplot as plt
from utils import Utils

def collect_data_from_csv_files(csv_files):
    collected_data = pd.DataFrame()
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        collected_data = pd.concat([collected_data, df])

    return collected_data

def get_winner(team_away, score_away, team_home, score_home):
    if score_away > score_home:
        return team_away
    return team_home

def get_winner_and_date(match_results_df: pd.DataFrame):
    match_results_df["Winner"] = match_results_df.apply(lambda game: get_winner(game["Visitor/Neutral"], game["PTS"], game["Home/Neutral"], game["PTS.1"]), axis=1)

    return match_results_df

# Example usage
directory = '.'  # Replace with your folder path
csv_files = Utils.get_csv_files_from_directory(directory)
data = collect_data_from_csv_files(csv_files=csv_files)

winners = get_winner_and_date(data)

winners["Date"] = pd.to_datetime(winners["Date"], format='%a, %b %d, %Y')

winner_date_df = winners[["Date", "Winner"]].groupby(["Date", "Winner"]).size().unstack(fill_value=0)

print(winner_date_df)

winner_date_df = winner_date_df.cumsum()

winner_date_df.plot(kind='line', marker='o')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Occurrences')
plt.title('Wins Over Time')
plt.xticks(rotation=45)
plt.legend().set_draggable(True)
plt.show()
