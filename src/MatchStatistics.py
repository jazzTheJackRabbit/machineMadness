import pandas as pd
import numpy as np
import re

# 
# Creates MATCH statistics for all tournament matches in a season (for all seasons)
# 

ROOT_DIR = "../"

def create(season_data_file_path,season_tournament_file_path,team_statistic_file_path,training_data_match_stats_file_path):
	season_statistics = pd.read_csv(ROOT_DIR+season_data_file_path);
	tournament_statistics = pd.read_csv(ROOT_DIR+season_tournament_file_path);
	team_statistics = pd.read_csv(ROOT_DIR+team_statistic_file_path);
	all_teams = pd.read_csv(ROOT_DIR+"data/raw/teams.csv")
	
	all_tournament_seasons = np.unique(tournament_statistics.season)
	training_data = pd.DataFrame()

	for season in all_tournament_seasons:
		print("Processing Data for :"+str(season))
		tournament_statistics_for_season = tournament_statistics[tournament_statistics.season == season]
		team_statistics_for_season = team_statistics[team_statistics.season == season]
		for index,row in tournament_statistics_for_season.iterrows():
		    tournament_match = row

		    #Find the two teams
		    winning_team_id = tournament_match['wteam']
		    losing_team_id =  tournament_match['lteam']

		    #Here, we enforce a convention for labeling: 
		    #Get their stats_vector from team_stats
		    if(winning_team_id < losing_team_id):
		        team1_statistic = team_statistics_for_season[team_statistics_for_season.teamId == winning_team_id]
		        team2_statistic = team_statistics_for_season[team_statistics_for_season.teamId == losing_team_id]
		        output_label = 0
		    else:
		        team1_statistic = team_statistics_for_season[team_statistics_for_season.teamId == losing_team_id]
		        team2_statistic = team_statistics_for_season[team_statistics_for_season.teamId == winning_team_id]
		        output_label = 1

		    team1_np_vector = team1_statistic[team1_statistic.columns[2:]].as_matrix()
		    team2_np_vector = team2_statistic[team2_statistic.columns[2:]].as_matrix()

		    #Find difference between the vectors
		    match_vector = team1_np_vector - team2_np_vector

		    #Take the difference vector and append it with the label it with 0 if first team won, and 1 if the second team won
		    team1 = winning_team_id if (winning_team_id < losing_team_id) else losing_team_id
		    team2 = winning_team_id if (winning_team_id > losing_team_id) else losing_team_id
		    match_team1_id = pd.DataFrame([team1],columns=["team1"])
		    match_team2_id = pd.DataFrame([team2],columns=["team2"])
		    match_statistics = pd.DataFrame(match_vector,columns=team1_statistic.columns[2:])
		    match_output_label = pd.DataFrame([output_label],columns=["winningTeam"])

		    row_vector_for_training_data = pd.concat([match_team1_id,match_team2_id,match_statistics,match_output_label],axis=1)
		    row_vector_for_training_data.season = season

		    # Append to training-data-for-season
		    training_data = training_data.append(row_vector_for_training_data,ignore_index=True)

	training_data.to_csv(ROOT_DIR+training_data_match_stats_file_path)
	print("Match Stats generated and Saved successfully @ "+ROOT_DIR+training_data_match_stats_file_path)
