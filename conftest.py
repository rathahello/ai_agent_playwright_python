"""Pytest fixtures and configuration for SauceDemo test suite."""

from collections.abc import Generator
from pathlib import Path
import sys

import pytest
from playwright.sync_api import Page

# Ensure project root is in sys.path for direct execution / IDE support
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.navigation_page import NavigationPage


@pytest.fixture
def login_page(page: Page) -> Generator[LoginPage, None, None]:
    """Provide an initialized LoginPage instance navigated to the login screen."""
    # Setup
    login_pg = LoginPage(page)
    login_pg.load()

    yield login_pg

    # Teardown: brief pause so the final UI state can be observed in headed mode
    page.wait_for_timeout(1500)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """Provide an initialized InventoryPage instance."""
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    """Provide an initialized CartPage instance."""
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    """Provide an initialized CheckoutPage instance."""
    return CheckoutPage(page)


@pytest.fixture
def navigation_page(page: Page) -> NavigationPage:
    """Provide an initialized NavigationPage instance."""
    return NavigationPage(page)



