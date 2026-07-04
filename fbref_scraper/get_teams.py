"""
fbref_scraper.get_teams
~~~~~~~~~~~~~~~~~~~~~~~~

Parses a league standings page's rendered HTML into a DataFrame of
squad ids and team names.
"""

import re

import pandas as pd
from bs4 import BeautifulSoup


def get_teams(html: str, league_slug: str, season: str) -> pd.DataFrame:
    """Parse the list of squads (team name + fbref squad id) out of a
    rendered league standings page.

    Parameters
    ----------
    html : str
        Fully rendered page HTML (from a league standings page, e.g.
        https://fbref.com/en/comps/9/2015-2016/2015-2016-Premier-League-Stats).
    league_slug : str
        Hyphenated league name, used only for naming the output CSV,
        e.g. "Premier-League".
    season : str
        e.g. "2015-2016". Used for naming the output CSV and stamping
        a 'season' column.

    Returns
    -------
    pd.DataFrame with columns: squad_id, team_name, season
    """
    soup = BeautifulSoup(html, "html.parser")

    all_team_cells = soup.find_all(attrs={"data-stat": "team"})
    team_cells = [c for c in all_team_cells if "left" in c.get("class", [])]

    print(
        f"Found {len(all_team_cells)} total data-stat='team' cells, "
        f"{len(team_cells)} with class 'left'"
    )

    rows = []
    for cell in team_cells:
        link = cell.find("a", href=re.compile(r"/en/squads/"))
        if link is None:
            continue
        team_name = link.get_text(strip=True)

        # Skip "vs" entries (opponent-facing rows in some tables,
        # not actual squad rows)
        if team_name.lower().startswith("vs"):
            continue

        match = re.search(r"/en/squads/([a-f0-9]+)/", link["href"])
        squad_id = match.group(1) if match else None
        rows.append({"squad_id": squad_id, "team_name": team_name})

    df = pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)
    df["season"] = season

    return df
