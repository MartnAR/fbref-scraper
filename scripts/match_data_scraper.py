from fbref_scraper import FbRefScraper
import pandas as pd

fb = FbRefScraper()

# Scrape matches data
teams = pd.read_csv("lic_team_data_2122.csv")

# Create empty data frame instance
matches = pd.DataFrame()

# Loop over team data for a season, return all matches played
for i in range(len(teams)):
    team = teams.loc[i, 'team_name']
    teamid = teams.loc[i, 'squad_id']
    league = teams.loc[i, 'league']
    season = '20' + teams.loc[i, 'season'].astype(str)[:2] + '-20' + teams.loc[i, 'season'].astype(str)[2:]

    team_matches = fb.get_matches(team=team, teamid=teamid, league=league, season=season)

    print(f"Match report for {team} in {season} obtained.")

    matches = pd.concat([matches, team_matches], axis=0)

matches.to_csv('lic_matches_2021_2022.csv', index=False)