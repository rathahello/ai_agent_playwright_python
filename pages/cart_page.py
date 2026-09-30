"""Page object for SauceDemo Shopping Cart Page."""

from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page object encapsulating the SauceDemo Cart page (/cart.html)."""

    PATH = "/cart.html"
    EXPECTED_URL = "https://www.saucedemo.com/cart.html"

    # Locators
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_DESC = ".inventory_item_desc"
    ITEM_PRICE = ".inventory_item_price"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_items: Locator = page.locator(self.CART_ITEM)
        self.item_names: Locator = page.locator(self.ITEM_NAME)
        self.cart_badge: Locator = page.locator(self.SHOPPING_CART_BADGE)
        self.cart_link: Locator = page.locator(self.SHOPPING_CART_LINK)
        self.checkout_button: Locator = page.locator(self.CHECKOUT_BUTTON)
        self.continue_shopping_button: Locator = page.locator(self.CONTINUE_SHOPPING_BUTTON)

    def load(self) -> None:
        """Navigate directly to the shopping cart page."""
        self.navigate(self.PATH)

    def open_cart(self) -> None:
        """Click the shopping cart link to navigate to the cart page."""
        self.cart_link.click()

    def remove_item(self, product_name: str) -> None:
        """Remove a product from the cart by its name."""
        self.cart_items.filter(has_text=product_name).get_by_role(
            "button", name="Remove"
        ).click()

    def get_item_count(self) -> int:
        """Return the number of items currently in the cart."""
        return self.cart_items.count()

    def click_checkout(self) -> None:
        """Click the checkout button to begin checkout process."""
        self.checkout_button.click()

    def click_continue_shopping(self) -> None:
        """Click the continue shopping button to return to products."""
        self.continue_shopping_button.click()
