from fbref_scraper import FbRefScraper
import pandas as pd
from pathlib import Path

# Load scraper
fb = FbRefScraper()

# Load match data
matches = pd.read_csv("lff_matches_2019_2025.csv")

# Obtain unique team, season values
team_season = matches[["team", "season"]].drop_duplicates(
    subset=["team", "season"]).values.tolist()

matches["team_game_id"] = matches["team"] + "-" + matches["match_id"]

for i, j in team_season: 
    # Create folder for each season
    i_team = i.replace(" ", "_")
    folder = f"lff/season_{j}/{i_team}"
    Path(folder).mkdir(parents=True, exist_ok=True)

    desc = matches[(matches["team"]==i) & (matches["season"]==j)].reset_index()
    for d in range(len(desc)):

        comp = desc.loc[d, "comp"].lower().replace(" ", "_")
        opponent = desc.loc[d, "opponent"].lower().replace(" ", "_")
        date = desc.loc[d, "match_date"]
        team_game_id = desc.loc[d, "team_game_id"]

        mr = fb.get_match_report(
            match_url=desc.loc[d, 'match_report'],
            team_name=desc.loc[d, 'team'],
            season=desc.loc[d, 'season'].astype(str),
            match_date=desc.loc[d, 'match_date'],
            comp=desc.loc[d, 'comp'],
            opponent=desc.loc[d, 'opponent'],
            venue=desc.loc[d, 'venue'],
            match_id=desc.loc[d, 'match_id']
        )

        # Bodø/Glimt having a forward slash in the name creates an escape clause situation. 
        # Code should be debugged at some point to clear any symbols and replace with _
        if '/' in opponent:
            opponent = opponent.replace("/", "_")

        if '/' in comp:
            comp = comp.replace('/', '_')

        mr.to_csv(f"{folder}/{comp}_{opponent}_{date}.csv")

        matches = matches[(matches["team_game_id"]!=team_game_id)]

        # Want to update list of matches that have yet to be scraped in case 
        # fbref/scraper crash. This way, user doesn't have to restart from 0. 
        matches.to_csv("lff_matches_2019_2025_updated.csv", index=False)
