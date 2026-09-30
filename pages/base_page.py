"""Base Page Object containing common actions and components."""

from playwright.sync_api import Page


class BasePage:
    BASE_URL = "https://www.saucedemo.com"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = ""):
        """Navigate to a URL relative to BASE_URL."""
        target_url = f"{self.BASE_URL}{path}"
        self.page.goto(target_url)

    @property
    def current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url
