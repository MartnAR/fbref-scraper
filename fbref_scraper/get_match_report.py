"""
fbref_scraper.get_match_report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parses a match report page's rendered HTML into a DataFrame of one
team's player stats summary table.
"""

import re

import pandas as pd
from bs4 import BeautifulSoup


def get_match_report(html: str, team_name: str) -> pd.DataFrame:
    """Parse a single team's player stats summary table out of a rendered
    match report page.

    Parameters
    ----------
    html : str
        Fully rendered page HTML (from a match report page, e.g.
        https://fbref.com/en/matches/a071faa8/Liverpool-Bournemouth-August-15-2025-Premier-League).
    team_name : str
        Team name as it appears in the table caption, e.g. "Liverpool".
        Used to disambiguate between the two teams' summary tables on
        the page, and for naming the output CSV.

    Returns
    -------
    pd.DataFrame of the player stats summary table for the given team.
    """
    soup = BeautifulSoup(html, "html.parser")

    summary_tables = soup.find_all(
        "table", class_="stats_table", id=re.compile(r"^stats_\w+_summary$")
    )

    target_table = None
    for table in summary_tables:
        caption = table.find("caption")
        if caption and team_name in caption.get_text():
            target_table = table
            break

    if target_table is None:
        raise ValueError(f"No summary stats table found for team '{team_name}'")

    df = pd.read_html(str(target_table))[0]

    return df
