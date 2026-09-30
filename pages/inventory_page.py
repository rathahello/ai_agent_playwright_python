"""Page object for SauceDemo Inventory / Products Page."""

from playwright.sync_api import Locator, Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page object encapsulating the SauceDemo Inventory / Products page."""

    PATH = "/inventory.html"
    EXPECTED_URL = "https://www.saucedemo.com/inventory.html"

    # Inventory Locators
    INVENTORY_LIST = ".inventory_list"
    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_DESC = ".inventory_item_desc"
    ITEM_PRICE = ".inventory_item_price"
    ITEM_IMAGE = ".inventory_item_img img"
    SORT_DROPDOWN = '[data-test="product-sort-container"]'
    APP_LOGO = ".app_logo"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"

    # Product Details Locators
    DETAILS_NAME = ".inventory_details_name"
    DETAILS_DESC = ".inventory_details_desc"
    DETAILS_PRICE = ".inventory_details_price"
    DETAILS_IMAGE = ".inventory_details_img"
    BACK_TO_PRODUCTS_BTN = "#back-to-products"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Catalog elements
        self.inventory_list: Locator = page.locator(self.INVENTORY_LIST)
        self.inventory_items: Locator = page.locator(self.INVENTORY_ITEM)
        self.item_names: Locator = page.locator(self.ITEM_NAME)
        self.item_descriptions: Locator = page.locator(self.ITEM_DESC)
        self.item_prices: Locator = page.locator(self.ITEM_PRICE)
        self.item_images: Locator = page.locator(self.ITEM_IMAGE)
        self.sort_dropdown: Locator = page.locator(self.SORT_DROPDOWN)
        self.app_logo: Locator = page.locator(self.APP_LOGO)
        self.cart_link: Locator = page.locator(self.SHOPPING_CART_LINK)
        self.cart_badge: Locator = page.locator(self.SHOPPING_CART_BADGE)

        # Details elements
        self.details_name: Locator = page.locator(self.DETAILS_NAME)
        self.details_desc: Locator = page.locator(self.DETAILS_DESC)
        self.details_price: Locator = page.locator(self.DETAILS_PRICE)
        self.details_image: Locator = page.locator(self.DETAILS_IMAGE)
        self.back_to_products_btn: Locator = page.locator(self.BACK_TO_PRODUCTS_BTN)

    def load(self) -> None:
        """Navigate directly to the inventory page."""
        self.navigate(self.PATH)

    def get_item(self, product_name: str) -> Locator:
        """Get the container locator for a specific product."""
        return self.inventory_items.filter(has_text=product_name)

    def get_button_for_product(self, product_name: str) -> Locator:
        """Get the action button ('Add to cart' or 'Remove') for a product."""
        return self.get_item(product_name).locator("button")

    def add_to_cart(self, product_name: str) -> None:
        """Click 'Add to cart' for the specified product name."""
        self.get_item(product_name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, product_name: str) -> None:
        """Click 'Remove' for the specified product name."""
        self.get_item(product_name).get_by_role("button", name="Remove").click()

    def open_cart(self) -> None:
        """Click the shopping cart link to navigate to the cart page."""
        self.cart_link.click()

    def select_sort_option(self, option_value: str) -> None:
        """Select a sort option: 'az', 'za', 'lohi', or 'hilo'."""
        self.sort_dropdown.select_option(option_value)

    def get_all_product_names(self) -> list[str]:
        """Return a list of all product name texts."""
        return self.item_names.all_inner_texts()

    def get_all_product_prices(self) -> list[float]:
        """Return a list of all product prices parsed as floats."""
        raw_prices = self.item_prices.all_inner_texts()
        return [float(p.replace("$", "").strip()) for p in raw_prices]

    def click_product_name(self, index: int = 0) -> None:
        """Click a product name link by its index (defaults to first item)."""
        self.item_names.nth(index).click()

    def click_back_to_products(self) -> None:
        """Click 'Back to products' button from details view."""
        self.back_to_products_btn.click()
