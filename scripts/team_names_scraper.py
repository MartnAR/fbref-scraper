from fbref_scraper import FbRefScraper
import pandas as pd
import time

fb = FbRefScraper()

# Scrape Teams per Season data
leagues = ["Premier League", "Serie A", "La Liga", "Ligue 1", "Bundesliga"]
seasons = ["2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"]

# Create empty data frame
teams = pd.DataFrame()

# Loop over every league and season to return all teams that played in the league in a season
for league in leagues: 
    for season in seasons: 
        team_names = fb.get_teams("league", seasons)
        teams = pd.concat([teams, team_names], axis=0)
        print(team_names.head())

        time.sleep(10)

    teams.to_csv(f"{league}_team_data_2019_2025.csv")
