from pathlib import Path
import sys

import pytest
from playwright.sync_api import Page, expect

# Ensure project root is in sys.path when running file directly or from IDE
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

# ---------------------------------------------------------------------------
# Test Data
# ---------------------------------------------------------------------------
STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------

@pytest.mark.cart
@pytest.mark.smoke
def test_tc_cart_001_add_item_to_cart_from_inventory(
    login_page: LoginPage, inventory_page: InventoryPage, cart_page: CartPage
) -> None:
    """TC-CART-001: Add Item to Cart from Inventory.

    Preconditions:
        User is logged in as standard_user and on the inventory page.
    Steps:
        1. Click 'Add to cart' on Sauce Labs Backpack.
    Expected:
        - Button text toggles to 'Remove'.
        - Shopping cart badge displays '1'.
    """
    # Arrange: Log in with standard user
    login_page.login(username=STANDARD_USER, password=PASSWORD)

    # Action: Click "Add to cart" on Backpack
    inventory_page.add_to_cart(BACKPACK)

    # Assertion: Verify button changed to 'Remove' and badge count is 1
    backpack_btn = inventory_page.get_button_for_product(BACKPACK)
    expect(backpack_btn).to_have_text("Remove")
    expect(cart_page.cart_badge).to_have_text("1")


@pytest.mark.cart
def test_tc_cart_002_remove_item_from_cart_on_inventory_page(
    login_page: LoginPage, inventory_page: InventoryPage, cart_page: CartPage
) -> None:
    """TC-CART-002: Remove Item from Cart on Inventory Page.

    Preconditions:
        User is logged in and an item is added to the cart.
    Steps:
        1. Click 'Remove' button on the item.
    Expected:
        - Button toggles back to 'Add to cart'.
        - Shopping cart badge disappears.
    """
    # Arrange: Log in and add item to cart
    login_page.login(username=STANDARD_USER, password=PASSWORD)
    inventory_page.add_to_cart(BACKPACK)
    expect(cart_page.cart_badge).to_have_text("1")

    # Action: Click "Remove" button on Backpack
    inventory_page.remove_from_cart(BACKPACK)

    # Assertion: Button toggles back to "Add to cart" and cart badge is removed
    backpack_btn = inventory_page.get_button_for_product(BACKPACK)
    expect(backpack_btn).to_have_text("Add to cart")
    expect(cart_page.cart_badge).to_have_count(0)


@pytest.mark.cart
@pytest.mark.smoke
def test_tc_cart_003_cart_persistence_across_pages(
    page: Page,
    login_page: LoginPage,
    inventory_page: InventoryPage,
    cart_page: CartPage,
) -> None:
    """TC-CART-003: Cart Persistence Across Pages.

    Preconditions:
        User is logged in and has 2 items added to cart from inventory.
    Steps:
        1. Click the shopping cart link.
    Expected:
        - Navigates to cart.html.
        - Displays exactly 2 cart items matching the added products.
    """
    # Arrange: Log in and add two items
    login_page.login(username=STANDARD_USER, password=PASSWORD)
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    expect(cart_page.cart_badge).to_have_text("2")

    # Action: Navigate to cart page
    cart_page.open_cart()

    # Assertion: URL is cart.html and contains the 2 items in order
    expect(page).to_have_url(cart_page.EXPECTED_URL)
    expect(cart_page.cart_items).to_have_count(2)
    expect(cart_page.item_names).to_have_text([BACKPACK, BIKE_LIGHT])


@pytest.mark.cart
def test_tc_cart_004_remove_item_from_cart_page(
    page: Page,
    login_page: LoginPage,
    inventory_page: InventoryPage,
    cart_page: CartPage,
) -> None:
    """TC-CART-004: Remove Item from Cart Page.

    Preconditions:
        User is logged in, has 2 items added, and is on cart.html.
    Steps:
        1. Click 'Remove' button on one item.
    Expected:
        - Cart item count drops from 2 to 1.
        - Shopping cart badge updates to '1'.
        - Remaining item is displayed correctly.
    """
    # Arrange: Log in, add 2 items, and go to cart page
    login_page.login(username=STANDARD_USER, password=PASSWORD)
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    cart_page.open_cart()
    expect(page).to_have_url(cart_page.EXPECTED_URL)
    expect(cart_page.cart_items).to_have_count(2)

    # Action: Remove Backpack from cart
    cart_page.remove_item(BACKPACK)

    # Assertion: Item count drops to 1, badge shows '1', and Bike Light remains
    expect(cart_page.cart_items).to_have_count(1)
    expect(cart_page.cart_badge).to_have_text("1")
    expect(cart_page.item_names).to_have_text([BIKE_LIGHT])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
