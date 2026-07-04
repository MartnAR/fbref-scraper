"""
fbref_scraper.fbref_scraper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FbRefScraper class: owns the browser session (Playwright over CDP, driven
by a SeleniumBase-managed Chrome instance), builds fbref URLs, fetches
rendered HTML, and delegates parsing to the get_teams / get_matches /
get_match_report functions.
"""

from playwright.sync_api import sync_playwright
from seleniumbase import sb_cdp

from .get_teams import get_teams
from .get_matches import get_matches
from .get_match_report import get_match_report

LEAGUES = {
    "Premier League": 9,
    "Serie A": 11,
    "La Liga": 12,
    "Ligue 1": 13,
    "Bundesliga": 20,
}


class FbRefScraper:
    """Scraper for teams, match schedules, and match report stat tables
    on fbref.com.

    Example
    -------
    >>> with FbRefScraper() as scraper:
    ...     teams = scraper.get_teams("Premier League", "2015-2016")
    ...     matches = scraper.get_matches("Leicester-City", "a2d435b3", "2015-2016")
    ...     stats = scraper.get_match_report(matches["match_report"].iloc[0], "Leicester City")
    """

    def __init__(self, headless: bool = False, wait_seconds: int = 10):
        """
        Parameters
        ----------
        headless : bool
            Whether to run Chrome headlessly. Some fbref pages behave
            differently headless vs. headed; default is headed (False).
        wait_seconds : int
            Default number of seconds to wait for JS-rendered content to
            load before reading page HTML. Individual methods may override
            this with a longer wait if needed.
        """
        self.sb = sb_cdp.Chrome(use_chromium=True, headless=headless)
        self.endpoint_url = self.sb.get_endpoint_url()
        self.wait_seconds = wait_seconds

    # -- context manager support -----------------------------------------

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Shut down the underlying browser session."""
        try:
            self.sb.driver.quit()
        except AttributeError:
            # fallback for seleniumbase versions where .driver isn't nested
            try:
                self.sb.quit()
            except Exception as e:
                print(f"Warning: error closing browser: {e}")
        except Exception as e:
            print(f"Warning: error closing browser: {e}")

    # -- internal helper --------------------------------------------------

    def _get_page_html(self, url: str, wait_seconds: int = None) -> str:
        """Navigate to a URL via the shared CDP-connected browser and return
        the fully rendered page HTML."""
        wait = wait_seconds if wait_seconds is not None else self.wait_seconds
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(self.endpoint_url)
            context = browser.contexts[0]
            page = context.pages[0]
            page.goto(url)
            self.sb.sleep(wait)
            html = page.content()
        return html

    # -- public methods (thin wrappers: fetch HTML, delegate to get_*) ---

    def get_teams(self, league: str, season: str):
        """Scrape the list of squads for a league/season. See
        fbref_scraper.get_teams.get_teams for details on the returned
        DataFrame."""
        comp = LEAGUES[league]
        league_slug = league.replace(" ", "-")
        url = f"https://fbref.com/en/comps/{comp}/{season}/{season}-{league_slug}-Stats"

        html = self._get_page_html(url, wait_seconds=20)
        return get_teams(html, league_slug=league_slug, season=season)

    def get_matches(self, team: str, teamid: str, season: str):
        """Scrape match report URLs for a team's season. See
        fbref_scraper.get_matches.get_matches for details on the returned
        DataFrame."""
        url = f"https://fbref.com/en/squads/{teamid}/{season}/{team}-Stats"

        html = self._get_page_html(url, wait_seconds=10)
        return get_matches(html, team=team, season=season)

    def get_match_report(self, match_url: str, team_name: str):
        """Scrape a single team's player stats summary table from a match
        report page. See fbref_scraper.get_match_report.get_match_report
        for details on the returned DataFrame."""
        html = self._get_page_html(match_url, wait_seconds=5)
        return get_match_report(html, team_name=team_name)
