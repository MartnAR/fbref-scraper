"""
fbref_scraper._utils
~~~~~~~~~~~~~~~~~~~~~

Small shared helpers used across the get_teams / get_matches /
get_match_report parsing functions.
"""

import re


def shorten_season(season: str) -> str:
    """Convert a full season string like "2025-2026" into its short form
    "2526" (last two digits of each year, concatenated).

    Idempotent: if the input doesn't contain a hyphen, it's assumed to
    already be in shortened form (or some other format that shouldn't be
    touched) and is returned unchanged. This makes it safe to call on a
    value that's already been through shorten_season once -- e.g. when a
    get_matches() result row's 'season' value is passed straight into
    get_match_report().

    Parameters
    ----------
    season : str
        Full season string, e.g. "2025-2026".

    Returns
    -------
    str
        Shortened season string, e.g. "2526". If the input contains a
        hyphen but doesn't resolve to two 4-digit years, falls back to
        whatever digit groups were found, or the original string
        unchanged if none were found at all.
    """
    if "-" not in season:
        return season

    matches = re.findall(r"\d{2}(\d{2})", season)
    if len(matches) >= 2:
        return matches[0] + matches[1]
    elif len(matches) == 1:
        return matches[0]
    return season
