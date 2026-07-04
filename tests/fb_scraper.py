from fbref_scraper import FbRefScraper

fb = FbRefScraper()
df = fb.get_matches('Leicester', "a2d435b3", "Premier League", "2015-2016")
print(df)
fb.close() 