from fbref_scraper.get_teams import FbRefScraper as fb

scraper = fb()
df = scraper.get_match_report('Leicester', 'https://fbref.com/en/matches/a6cda14d/Leicester-City-Sunderland-August-8-2015-Premier-League')
scraper.close() 