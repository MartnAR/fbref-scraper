"""
fbref_scraper.get_matches
~~~~~~~~~~~~~~~~~~~~~~~~~~

Parses a team's season page's rendered HTML into a DataFrame of match
report URLs, along with the surrounding match metadata (date, competition,
venue, opponent, etc.) pulled from the same table row.
"""

import re

import pandas as pd
from bs4 import BeautifulSoup

from ._utils import shorten_season


def get_matches(html: str, team: str, league: str, season: str) -> pd.DataFrame:
    """Parse match report URLs and match metadata out of a rendered team
    season ("Scores & Fixtures") page.

    Parameters
    ----------
    html : str
        Fully rendered page HTML (from a team season page, e.g.
        https://fbref.com/en/squads/a2d435b3/2015-2016/Leicester-City-Stats).
    team : str
        Hyphenated team name as it appears in the fbref URL,
        e.g. "Leicester-City". Stamped as a 'team' column.
    league : str
        League name, e.g. "Premier League". This isn't present in the
        match row itself (the row's own "comp" cell reflects whichever
        competition that specific fixture belongs to, e.g. a match row
        might be an FA Cup game even on a Premier League team's page),
        so it's passed in explicitly and stamped onto every row.
    season : str
        Full season string, e.g. "2015-2016". Stamped as a 'season'
        column in shortened form (e.g. "1516").

    Returns
    -------
    pd.DataFrame with columns:
        league, season, team, match_date, comp, venue, opponent,
        match_id, match_report
    """
    soup = BeautifulSoup(html, "html.parser")

    # No class filter: data-stat is specific enough on its own, and the
    # class on this cell varies by table (often "center", not "left")
    match_cells = soup.find_all(attrs={"data-stat": "match_report"})

    print(f"Found {len(match_cells)} data-stat='match_report' cells")

    def _cell_text(row, data_stat):
        """Get stripped text from a sibling cell in the same row by its
        data-stat attribute, or None if that cell isn't present."""
        cell = row.find(attrs={"data-stat": data_stat})
        return cell.get_text(strip=True) if cell else None

    rows = []
    for cell in match_cells:
        link = cell.find("a", href=re.compile(r"/en/matches/\S+"))
        if link is None:
            continue
        match_url = "https://fbref.com" + link["href"]

        # Match id is the hex string in the match report URL, e.g.
        # /en/matches/a071faa8/Liverpool-Bournemouth-... -> "a071faa8"
        match_id_search = re.search(r"/en/matches/([a-z0-9]+)/", link["href"])
        match_id = match_id_search.group(1) if match_id_search else None

        row = cell.find_parent("tr")
        if row is None:
            continue

        rows.append(
            {
                "league": league,
                "season": shorten_season(season),
                "team": team,
                "match_date": _cell_text(row, "date"),
                "comp": _cell_text(row, "comp"),
                "venue": _cell_text(row, "venue"),
                "opponent": _cell_text(row, "opponent"),
                "match_id": match_id,
                "match_report": match_url,
            }
        )

    df = pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)

    return df
