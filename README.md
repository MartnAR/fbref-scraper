# fbref-scraper

A small Python package for scraping team lists, match schedules, and match
report player-stat tables from [fbref.com](https://fbref.com), using
Playwright connected over CDP to a SeleniumBase-managed Chrome instance
(this avoids most basic bot-detection issues on the site).

## Installation

Clone the repo and install locally:

```bash
git clone https://github.com/yourusername/fbref-scraper.git
cd fbref-scraper
pip install -e .
```

You'll also need Playwright's browser binaries installed once:

```bash
playwright install chromium
```

## Usage

```python
from fbref_scraper import FbRefScraper

with FbRefScraper() as scraper:
    # 1. Get all teams (squad id + name) in a league/season
    teams = scraper.get_teams("Premier League", "2015-2016")

    # 2. Get match report URLs for a specific team's season
    matches = scraper.get_matches("Leicester-City", "a2d435b3", "2015-2016")

    # 3. Get a team's player stats table from a single match report
    stats = scraper.get_match_report(
        matches["match_report"].iloc[0],
        team_name="Leicester City",
    )
```

Each method:
- Returns a `pandas.DataFrame`
- Saves a CSV to the current working directory by default (pass
  `save_csv=False` to skip this)

## Supported leagues

Defined in `fbref_scraper.LEAGUES`:

| League          | fbref comp id |
|-----------------|---------------|
| Premier League  | 9             |
| Serie A         | 11            |
| La Liga         | 12            |
| Ligue 1         | 13            |
| Bundesliga      | 20            |

## Notes / caveats

- fbref's page structure occasionally changes; if a method returns an
  empty DataFrame, check that the relevant `data-stat` attributes and
  table `id` patterns referenced in `scraper.py` still match the live
  page's HTML.
- Be a good citizen: fbref has a documented rate limit that will
  temporarily block your IP if you scrape too aggressively. Consider
  adding delays between calls if scraping many teams/matches in a loop.
- This project is not affiliated with or endorsed by Sports Reference LLC
  (fbref.com's operator). Check fbref's terms of use before large-scale
  scraping.

## License

MIT
