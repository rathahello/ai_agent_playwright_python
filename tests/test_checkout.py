"""Test cases for SauceDemo Checkout Flow (TC-CHK-001 to TC-CHK-003)."""

from pathlib import Path
import sys

import pytest
from playwright.sync_api import Page, expect

# Ensure project root is in sys.path when running file directly or from IDE
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

# ---------------------------------------------------------------------------
# Test Data & Constants
# ---------------------------------------------------------------------------
STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"
BACKPACK = "Sauce Labs Backpack"

FIRST_NAME = "John"
LAST_NAME = "Doe"
POSTAL_CODE = "12345"

FIRST_NAME_REQUIRED_ERROR = "Error: First Name is required"
LAST_NAME_REQUIRED_ERROR = "Error: Last Name is required"
POSTAL_CODE_REQUIRED_ERROR = "Error: Postal Code is required"
COMPLETE_ORDER_MESSAGE = "Thank you for your order!"


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------

@pytest.mark.checkout
@pytest.mark.smoke
def test_tc_chk_001_successful_checkout(
    page: Page,
    login_page: LoginPage,
    inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage,
) -> None:
    """TC-CHK-001: End-to-End Successful Checkout.

    Preconditions:
        User is logged in, has at least 1 item in cart, and is on cart.html.
    Steps:
        1. Click Checkout on the cart page.
        2. Fill First Name, Last Name, and Postal Code.
        3. Click Continue.
        4. Verify item total + tax matches total amount on Step Two.
        5. Click Finish.
    Expected:
        - URL is checkout-complete.html.
        - Header displays 'Thank you for your order!'.
        - Shopping cart badge is cleared.
    """
    # Arrange: Log in, add item to cart, and navigate to cart page
    login_page.login(username=STANDARD_USER, password=PASSWORD)
    inventory_page.add_to_cart(BACKPACK)
    cart_page.open_cart()
    expect(page).to_have_url(cart_page.EXPECTED_URL)

    # Action 1: Click checkout to go to Step One
    cart_page.click_checkout()
    expect(page).to_have_url(checkout_page.STEP_ONE_URL)

    # Action 2: Fill information and continue to Step Two
    checkout_page.fill_information(
        first_name=FIRST_NAME, last_name=LAST_NAME, postal_code=POSTAL_CODE
    )
    checkout_page.click_continue()
    expect(page).to_have_url(checkout_page.STEP_TWO_URL)

    # Assertion 1: Verify total calculation (subtotal + tax == total)
    subtotal = checkout_page.get_subtotal_amount()
    tax = checkout_page.get_tax_amount()
    total = checkout_page.get_total_amount()
    assert round(subtotal + tax, 2) == round(total, 2), (
        f"Subtotal ({subtotal}) + Tax ({tax}) does not equal Total ({total})"
    )

    # Action 3: Click Finish
    checkout_page.click_finish()

    # Assertion 2: Verify completion URL, message, and cleared cart
    expect(page).to_have_url(checkout_page.COMPLETE_URL)
    expect(checkout_page.complete_header).to_contain_text(COMPLETE_ORDER_MESSAGE)
    expect(checkout_page.cart_badge).to_have_count(0)


@pytest.mark.checkout
@pytest.mark.negative
def test_tc_chk_002_validation_missing_required_fields(
    page: Page,
    login_page: LoginPage,
    inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage,
) -> None:
    """TC-CHK-002: Checkout Validation - Missing Required Fields.

    Preconditions:
        User is navigated to checkout-step-one.html.
    Steps:
        1. Leave all fields blank and click Continue.
        2. Fill First Name only, click Continue.
        3. Fill First Name and Last Name, leave Postal Code blank, click Continue.
    Expected:
        - Appropriate error messages for each missing required field.
    """
    # Arrange: Log in, add item, navigate to Checkout Step One
    login_page.login(username=STANDARD_USER, password=PASSWORD)
    inventory_page.add_to_cart(BACKPACK)
    cart_page.open_cart()
    cart_page.click_checkout()
    expect(page).to_have_url(checkout_page.STEP_ONE_URL)

    # Step 1: All fields empty -> First Name required error
    checkout_page.click_continue()
    expect(checkout_page.error_message).to_be_visible()
    expect(checkout_page.error_message).to_contain_text(FIRST_NAME_REQUIRED_ERROR)

    # Step 2: Fill First Name only -> Last Name required error
    checkout_page.fill_information(first_name=FIRST_NAME)
    checkout_page.click_continue()
    expect(checkout_page.error_message).to_be_visible()
    expect(checkout_page.error_message).to_contain_text(LAST_NAME_REQUIRED_ERROR)

    # Step 3: Fill Last Name only, Postal Code empty -> Postal Code required error
    checkout_page.fill_information(last_name=LAST_NAME)
    checkout_page.click_continue()
    expect(checkout_page.error_message).to_be_visible()
    expect(checkout_page.error_message).to_contain_text(POSTAL_CODE_REQUIRED_ERROR)


@pytest.mark.checkout
def test_tc_chk_003_cancel_checkout_flow(
    page: Page,
    login_page: LoginPage,
    inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage,
) -> None:
    """TC-CHK-003: Cancel Checkout Flow.

    Preconditions:
        User is on checkout-step-one.html with items in cart.
    Steps:
        1. Click Cancel button.
    Expected:
        - User is returned to cart.html.
        - Cart items and cart badge remain intact.
    """
    # Arrange: Log in, add item, go to Checkout Step One
    login_page.login(username=STANDARD_USER, password=PASSWORD)
    inventory_page.add_to_cart(BACKPACK)
    cart_page.open_cart()
    cart_page.click_checkout()
    expect(page).to_have_url(checkout_page.STEP_ONE_URL)

    # Action: Click Cancel
    checkout_page.click_cancel()

    # Assertion: Returned to cart page with items intact
    expect(page).to_have_url(cart_page.EXPECTED_URL)
    expect(cart_page.cart_items).to_have_count(1)
    expect(cart_page.item_names).to_have_text([BACKPACK])
    expect(cart_page.cart_badge).to_have_text("1")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
