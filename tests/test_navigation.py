"""Test cases for SauceDemo Navigation & Session Controls (TC-NAV-001 to TC-NAV-002)."""

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
from pages.navigation_page import NavigationPage

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

@pytest.mark.navigation
@pytest.mark.smoke
def test_tc_nav_001_sidebar_logout(
    page: Page, login_page: LoginPage, navigation_page: NavigationPage
) -> None:
    """TC-NAV-001: Sidebar Logout.

    Preconditions:
        User is logged in as standard_user on inventory page.
    Steps:
        1. Open sidebar menu.
        2. Wait for Logout link to be visible and click it.
    Expected:
        - Redirected to login page (https://www.saucedemo.com/).
        - Login button is visible.
    """
    # Arrange: Log in
    login_page.login(username=STANDARD_USER, password=PASSWORD)

    # Action: Perform logout via NavigationPage
    navigation_page.logout()

    # Assertion: Redirected to login screen and login button is visible
    expect(page).to_have_url(login_page.BASE_URL + "/")
    expect(login_page.login_button).to_be_visible()


@pytest.mark.navigation
def test_tc_nav_002_reset_app_state(
    page: Page,
    login_page: LoginPage,
    inventory_page: InventoryPage,
    cart_page: CartPage,
    navigation_page: NavigationPage,
) -> None:
    """TC-NAV-002: Reset App State.

    Preconditions:
        User is logged in with 2 items added to cart.
    Steps:
        1. Open sidebar menu.
        2. Click Reset App State.
    Expected:
        - Cart badge is removed from the header.
        - Cart page has 0 items.
    """
    # Arrange: Log in and add 2 items to the cart
    login_page.login(username=STANDARD_USER, password=PASSWORD)
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    expect(cart_page.cart_badge).to_have_text("2")

    # Action: Reset App State via NavigationPage
    navigation_page.reset_app_state()

    # Assertion 1: Cart badge is immediately removed from header
    expect(cart_page.cart_badge).to_have_count(0)

    # Assertion 2: Navigate to cart page and verify 0 cart items
    cart_page.open_cart()
    expect(page).to_have_url(cart_page.EXPECTED_URL)
    expect(cart_page.cart_items).to_have_count(0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
