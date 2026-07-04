from fbref_scraper import FbRefScraper
import pandas as pd

fb = FbRefScraper()
#df = fb.get_matches('Liverpool', "822bd0ba", "Premier League", "2024-2025")
#df.to_csv("liverpool_2425_match_info.csv")

df = pd.read_csv("liverpool_2425_match_info.csv")

d = df.iloc[0]
print(d)

mr = fb.get_match_report(
    match_url=d['match_report'],
    team_name=d['team'],
    season=d['season'],
    match_date=d['match_date'],
    comp=d['comp'],
    opponent=d['opponent'],
    venue=d['venue'],
    match_id=d['match_id']
)

print(mr)
mr.to_csv("liverpool_2425_match_report_first_game.csv")

fb.close()