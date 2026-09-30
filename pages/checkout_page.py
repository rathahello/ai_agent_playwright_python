"""Page object for SauceDemo Checkout Flow Pages."""

import re
from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page object encapsulating SauceDemo Checkout steps (One, Two, and Complete)."""

    STEP_ONE_URL = "https://www.saucedemo.com/checkout-step-one.html"
    STEP_TWO_URL = "https://www.saucedemo.com/checkout-step-two.html"
    COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"

    # Step One Locators
    FIRST_NAME_INPUT = '[data-test="firstName"]'
    LAST_NAME_INPUT = '[data-test="lastName"]'
    POSTAL_CODE_INPUT = '[data-test="postalCode"]'
    CONTINUE_BUTTON = "#continue"
    CANCEL_BUTTON = "#cancel"
    ERROR_MESSAGE = '[data-test="error"]'

    # Step Two Locators
    SUBTOTAL_LABEL = ".summary_subtotal_label"
    TAX_LABEL = ".summary_tax_label"
    TOTAL_LABEL = ".summary_total_label"
    FINISH_BUTTON = "#finish"

    # Complete Locators
    COMPLETE_HEADER = ".complete-header"
    BACK_HOME_BUTTON = "#back-to-products"
    CART_BADGE = ".shopping_cart_badge"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Step One elements
        self.first_name_input: Locator = page.locator(self.FIRST_NAME_INPUT)
        self.last_name_input: Locator = page.locator(self.LAST_NAME_INPUT)
        self.postal_code_input: Locator = page.locator(self.POSTAL_CODE_INPUT)
        self.continue_button: Locator = page.locator(self.CONTINUE_BUTTON)
        self.cancel_button: Locator = page.locator(self.CANCEL_BUTTON)
        self.error_message: Locator = page.locator(self.ERROR_MESSAGE)

        # Step Two elements
        self.subtotal_label: Locator = page.locator(self.SUBTOTAL_LABEL)
        self.tax_label: Locator = page.locator(self.TAX_LABEL)
        self.total_label: Locator = page.locator(self.TOTAL_LABEL)
        self.finish_button: Locator = page.locator(self.FINISH_BUTTON)

        # Complete elements
        self.complete_header: Locator = page.locator(self.COMPLETE_HEADER)
        self.back_home_button: Locator = page.locator(self.BACK_HOME_BUTTON)
        self.cart_badge: Locator = page.locator(self.CART_BADGE)

    def load_step_one(self) -> None:
        """Navigate directly to Checkout Step One."""
        self.navigate("/checkout-step-one.html")

    def fill_information(
        self, first_name: str = "", last_name: str = "", postal_code: str = ""
    ) -> None:
        """Fill customer information fields on Step One."""
        if first_name:
            self.first_name_input.fill(first_name)
        if last_name:
            self.last_name_input.fill(last_name)
        if postal_code:
            self.postal_code_input.fill(postal_code)

    def click_continue(self) -> None:
        """Click Continue button on Step One."""
        self.continue_button.click()

    def click_cancel(self) -> None:
        """Click Cancel button."""
        self.cancel_button.click()

    def click_finish(self) -> None:
        """Click Finish button on Step Two."""
        self.finish_button.click()

    def get_subtotal_amount(self) -> float:
        """Extract numeric subtotal from summary subtotal label."""
        text = self.subtotal_label.inner_text()
        match = re.search(r"(\d+\.\d{2})", text)
        return float(match.group(1)) if match else 0.0

    def get_tax_amount(self) -> float:
        """Extract numeric tax from summary tax label."""
        text = self.tax_label.inner_text()
        match = re.search(r"(\d+\.\d{2})", text)
        return float(match.group(1)) if match else 0.0

    def get_total_amount(self) -> float:
        """Extract numeric total from summary total label."""
        text = self.total_label.inner_text()
        match = re.search(r"(\d+\.\d{2})", text)
        return float(match.group(1)) if match else 0.0

    def get_error_text(self) -> str:
        """Retrieve error banner text."""
        return self.error_message.inner_text()
