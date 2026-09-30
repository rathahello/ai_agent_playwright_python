"""Page object for SauceDemo Login Page."""

from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object encapsulating the SauceDemo Login page elements and actions."""

    # Locators
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = '[data-test="error"]'
    APP_LOGO = ".app_logo"
    INVENTORY_LIST = ".inventory_list"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input: Locator = page.locator(self.USERNAME_INPUT)
        self.password_input: Locator = page.locator(self.PASSWORD_INPUT)
        self.login_button: Locator = page.locator(self.LOGIN_BUTTON)
        self.error_message: Locator = page.locator(self.ERROR_MESSAGE)
        self.app_logo: Locator = page.locator(self.APP_LOGO)
        self.inventory_list: Locator = page.locator(self.INVENTORY_LIST)

    def load(self) -> None:
        """Navigate to the login page."""
        self.navigate("/")

    def enter_username(self, username: str) -> None:
        """Fill username input field."""
        self.username_input.fill(username)

    def enter_password(self, password: str) -> None:
        """Fill password input field."""
        self.password_input.fill(password)

    def click_login(self) -> None:
        """Click the login button."""
        self.login_button.click()

    def login(self, username: str = "", password: str = "") -> None:
        """Perform login action with the provided credentials."""
        if username:
            self.enter_username(username)
        if password:
            self.enter_password(password)
        self.click_login()

    def get_error_text(self) -> str:
        """Retrieve the text content of the error banner."""
        return self.error_message.inner_text()

