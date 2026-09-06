from fbref_scraper import FbRefScraper
import pandas as pd
import time

fb = FbRefScraper()

# Scrape Teams per Season data
# leagues = ["Premier League", "Serie A", "La Liga", "Ligue 1", "Bundesliga"]
# seasons = ["2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"]

# teams = pd.DataFrame()

# #for league in leagues: 
# for season in seasons: 
#     team_names = fb.get_teams("Bundesliga", season)
#     teams = pd.concat([teams, team_names], axis=0)
#     print(team_names.head())

#     time.sleep(10)

# teams.to_csv("dbl_team_data.csv")

# Scrape matches data
teams = pd.read_csv("lff_team_data.csv")

matches = pd.DataFrame()

for i in range(len(teams)):
    team = teams.loc[i, 'team_name']
    teamid = teams.loc[i, 'squad_id']
    league = teams.loc[i, 'league']
    season = '20' + teams.loc[i, 'season'].astype(str)[:2] + '-20' + teams.loc[i, 'season'].astype(str)[2:]

    team_matches = fb.get_matches(team=team, teamid=teamid, league=league, season=season)

    print(f"Match report for {team} in {season} obtained.")

    matches = pd.concat([matches, team_matches], axis=0)

matches.to_csv('lff_matches_2019_2025.csv', index=False)

#epl = fb.get_teams("Premier League", "2019-2020")
#print(epl.head())
#df = fb.get_matches('Liverpool', "822bd0ba", "Premier League", "2024-2025")
#df.to_csv("liverpool_2425_match_info.csv")
