"""Test cases for SauceDemo Inventory & Products (TC-INV-001 to TC-INV-004)."""

import re
from pathlib import Path
import sys

import pytest
from playwright.sync_api import Page, expect

# Ensure project root is in sys.path when running file directly or from IDE
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

# ---------------------------------------------------------------------------
# Test Data
# ---------------------------------------------------------------------------
STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"
EXPECTED_ITEM_COUNT = 6


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------

@pytest.mark.inventory
@pytest.mark.smoke
def test_tc_inv_001_verify_inventory_items_display(
    login_page: LoginPage, inventory_page: InventoryPage
) -> None:
    """TC-INV-001: Verify Inventory Items Display.

    Preconditions:
        User is logged in as standard_user.
    Steps:
        1. Inspect the inventory item collection.
    Expected:
        - Exactly 6 items are displayed.
        - Every item has a non-empty name, description, price, and image.
    """
    # Arrange: Log in
    login_page.login(username=STANDARD_USER, password=PASSWORD)

    # Assertion 1: Total count of inventory items equals 6
    expect(inventory_page.inventory_items).to_have_count(EXPECTED_ITEM_COUNT)

    # Assertion 2: Verify each individual item has complete information
    for index in range(EXPECTED_ITEM_COUNT):
        item = inventory_page.inventory_items.nth(index)
        name = item.locator(inventory_page.ITEM_NAME)
        desc = item.locator(inventory_page.ITEM_DESC)
        price = item.locator(inventory_page.ITEM_PRICE)
        image = item.locator(inventory_page.ITEM_IMAGE)

        expect(name).not_to_be_empty()
        expect(desc).not_to_be_empty()
        expect(price).not_to_be_empty()
        expect(image).to_be_visible()


@pytest.mark.inventory
def test_tc_inv_002_product_sorting_name(
    login_page: LoginPage, inventory_page: InventoryPage
) -> None:
    """TC-INV-002: Product Sorting - Name (A to Z) & (Z to A).

    Preconditions:
        User is logged in as standard_user.
    Steps:
        1. Select sort option 'az'.
        2. Verify names are in ascending alphabetical order.
        3. Select sort option 'za'.
        4. Verify names are in descending alphabetical order.
    """
    # Arrange: Log in
    login_page.login(username=STANDARD_USER, password=PASSWORD)

    # Action 1: Sort Name (A to Z)
    inventory_page.select_sort_option("az")
    names_az = inventory_page.get_all_product_names()

    # Assertion 1: Verify ascending alphabetical order
    assert names_az == sorted(names_az), f"Items not sorted A-Z: {names_az}"

    # Action 2: Sort Name (Z to A)
    inventory_page.select_sort_option("za")
    names_za = inventory_page.get_all_product_names()

    # Assertion 2: Verify descending alphabetical order
    assert names_za == sorted(names_za, reverse=True), f"Items not sorted Z-A: {names_za}"


@pytest.mark.inventory
def test_tc_inv_003_product_sorting_price(
    login_page: LoginPage, inventory_page: InventoryPage
) -> None:
    """TC-INV-003: Product Sorting - Price (Low to High) & (High to Low).

    Preconditions:
        User is logged in as standard_user.
    Steps:
        1. Select sort option 'lohi'.
        2. Verify prices are in ascending numerical order.
        3. Select sort option 'hilo'.
        4. Verify prices are in descending numerical order.
    """
    # Arrange: Log in
    login_page.login(username=STANDARD_USER, password=PASSWORD)

    # Action 1: Sort Price (Low to High)
    inventory_page.select_sort_option("lohi")
    prices_lohi = inventory_page.get_all_product_prices()

    # Assertion 1: Verify ascending order
    assert prices_lohi == sorted(prices_lohi), f"Prices not sorted Low-High: {prices_lohi}"

    # Action 2: Sort Price (High to Low)
    inventory_page.select_sort_option("hilo")
    prices_hilo = inventory_page.get_all_product_prices()

    # Assertion 2: Verify descending order
    assert prices_hilo == sorted(prices_hilo, reverse=True), f"Prices not sorted High-Low: {prices_hilo}"


@pytest.mark.inventory
def test_tc_inv_004_view_product_details(
    page: Page, login_page: LoginPage, inventory_page: InventoryPage
) -> None:
    """TC-INV-004: View Product Details.

    Preconditions:
        User is logged in as standard_user.
    Steps:
        1. Click first product name in inventory.
    Expected:
        - Navigates to inventory-item.html?id=<id>.
        - Details page displays non-empty name, description, price.
        - 'Back to products' button is visible.
    """
    # Arrange: Log in and capture first product's expected title
    login_page.login(username=STANDARD_USER, password=PASSWORD)
    first_product_name = inventory_page.get_all_product_names()[0]

    # Action: Click the first product name
    inventory_page.click_product_name(0)

    # Assertion: Verify URL and details display
    expect(page).to_have_url(re.compile(r".*inventory-item\.html\?id=\d+"))
    expect(inventory_page.details_name).to_have_text(first_product_name)
    expect(inventory_page.details_desc).not_to_be_empty()
    expect(inventory_page.details_price).not_to_be_empty()
    expect(inventory_page.back_to_products_btn).to_be_visible()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
