"""Page object for SauceDemo Navigation and Sidebar Controls."""

from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class NavigationPage(BasePage):
    """Page object encapsulating the sidebar menu navigation and session controls."""

    # Selectors
    BURGER_MENU_BTN = "#react-burger-menu-btn"
    BURGER_CROSS_BTN = "#react-burger-cross-btn"
    ALL_ITEMS_LINK = "#inventory_sidebar_link"
    ABOUT_LINK = "#about_sidebar_link"
    LOGOUT_LINK = "#logout_sidebar_link"
    RESET_APP_STATE_LINK = "#reset_sidebar_link"
    MENU_CONTAINER = ".bm-menu-wrap"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.menu_button: Locator = page.locator(self.BURGER_MENU_BTN)
        self.close_button: Locator = page.locator(self.BURGER_CROSS_BTN)
        self.all_items_link: Locator = page.locator(self.ALL_ITEMS_LINK)
        self.about_link: Locator = page.locator(self.ABOUT_LINK)
        self.logout_link: Locator = page.locator(self.LOGOUT_LINK)
        self.reset_link: Locator = page.locator(self.RESET_APP_STATE_LINK)
        self.menu_container: Locator = page.locator(self.MENU_CONTAINER)

    def open_menu(self) -> None:
        """Open the burger sidebar menu and wait for it to become visible."""
        self.menu_button.click()
        self.logout_link.wait_for(state="visible")

    def close_menu(self) -> None:
        """Close the burger sidebar menu."""
        self.close_button.click()

    def logout(self) -> None:
        """Open the sidebar menu and click Logout."""
        self.open_menu()
        self.logout_link.click()

    def reset_app_state(self) -> None:
        """Open the sidebar menu and click Reset App State."""
        self.open_menu()
        self.reset_link.click()
        self.close_menu()
