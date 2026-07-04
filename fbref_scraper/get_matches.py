"""
fbref_scraper.get_matches
~~~~~~~~~~~~~~~~~~~~~~~~~~

Parses a team's season page's rendered HTML into a DataFrame of match
report URLs.
"""

import re

import pandas as pd
from bs4 import BeautifulSoup


def get_matches(html: str, team: str, season: str) -> pd.DataFrame:
    """Parse match report URLs out of a rendered team season page.

    Parameters
    ----------
    html : str
        Fully rendered page HTML (from a team season page, e.g.
        https://fbref.com/en/squads/a2d435b3/2015-2016/Leicester-City-Stats).
    team : str
        Hyphenated team name as it appears in the fbref URL,
        e.g. "Leicester-City". Used for naming the output CSV and
        stamping a 'team' column.
    season : str
        e.g. "2015-2016". Used for naming the output CSV and stamping
        a 'season' column.

    Returns
    -------
    pd.DataFrame with columns: team, match_report, season
    """
    soup = BeautifulSoup(html, "html.parser")

    # No class filter: data-stat is specific enough on its own, and the
    # class on this cell varies by table (often "center", not "left")
    match_cells = soup.find_all(attrs={"data-stat": "match_report"})

    print(f"Found {len(match_cells)} data-stat='match_report' cells")

    rows = []
    for cell in match_cells:
        link = cell.find("a", href=re.compile(r"/en/matches/\S+"))
        if link is None:
            continue
        match_url = "https://fbref.com" + link["href"]
        rows.append({"team": team, "match_report": match_url})

    df = pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)
    df["season"] = season

    return df
