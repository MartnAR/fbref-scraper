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

    # 2. Get match report URLs + metadata for a specific team's season
    matches = scraper.get_matches(
        "Leicester-City", "a2d435b3", "Premier League", "2015-2016"
    )

    # 3. Get a team's player stats table from a single match report,
    #    stamped with that match's metadata (typically taken straight
    #    from the corresponding row of get_matches() output)
    row = matches.iloc[0]
    stats = scraper.get_match_report(
        row["match_report"],
        team_name="Leicester City",
        season=row["season"],
        match_date=row["match_date"],
        comp=row["comp"],
        opponent=row["opponent"],
        venue=row["venue"],
        match_id=row["match_id"],
    )
```

Each method returns a `pandas.DataFrame`. None of the methods write to
disk — save results yourself with `df.to_csv(...)` if needed.

### Standalone parsing (no browser required)

The three `get_*` functions that do the actual HTML parsing
(`get_teams`, `get_matches`, `get_match_report`) live in their own
modules and only depend on `beautifulsoup4`/`pandas` — not on
Playwright or SeleniumBase. If you already have rendered HTML (e.g.
saved from a previous scrape, or fetched some other way), you can call
them directly without spinning up a browser at all:

```python
from fbref_scraper.get_teams import get_teams

df = get_teams(html, league_slug="Premier-League", season="2015-2016")
```

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
  table `id` patterns referenced in the `get_*.py` modules still match
  the live page's HTML.
- Be a good citizen: fbref has a documented rate limit that will
  temporarily block your IP if you scrape too aggressively. Consider
  adding delays between calls if scraping many teams/matches in a loop.
- This project is not affiliated with or endorsed by Sports Reference LLC
  (fbref.com's operator). Check fbref's terms of use before large-scale
  scraping.

## License

MIT
