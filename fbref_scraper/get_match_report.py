"""
fbref_scraper.get_match_report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parses a match report page's rendered HTML into a DataFrame of one
team's player stats summary table, stamped with the match metadata
(season, date, competition, opponent, venue, match id) it was scraped
under.
"""

import io
import re

import pandas as pd
from bs4 import BeautifulSoup


def get_match_report(
    html: str,
    team_name: str,
    season: str,
    match_date: str,
    comp: str,
    opponent: str,
    venue: str,
    match_id: str,
) -> pd.DataFrame:
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
        the page, and stamped as a 'team_name' column.
    season, match_date, comp, opponent, venue, match_id : str
        Match metadata (typically taken from the corresponding row of
        get_matches() output) stamped onto every row of the returned
        table, so each player-stats row is fully labeled without needing
        a separate join back to the schedule table.

    Returns
    -------
    pd.DataFrame of the player stats summary table for the given team,
    with metadata columns prepended and the table's totals/footer row
    excluded.
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

    # Drop the <tfoot> totals row (e.g. "16 Players") before parsing, so
    # it never ends up as a row in the DataFrame
    tfoot = target_table.find("tfoot")
    if tfoot is not None:
        tfoot.decompose()

    s1 = re.findall(r'\d{2}(\d{2})', season)[0]
    s2 = re.findall(r'\d{2}(\d{2})', season)[1]
    s = s1+s2

    df = pd.read_html(io.StringIO(str(target_table)))[0]

    df.insert(0, "team_name", team_name)
    df.insert(1, "season", s)
    df.insert(2, "match_date", match_date)
    df.insert(3, "comp", comp)
    df.insert(4, "opponent", opponent)
    df.insert(5, "venue", venue)
    df.insert(6, "match_id", match_id)

    return df
