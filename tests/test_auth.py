"""Test cases for SauceDemo Authentication (TC-AUTH-001 to TC-AUTH-005)."""

from pathlib import Path
import sys

import pytest
from playwright.sync_api import Page, expect

# Ensure project root is in sys.path when running file directly or from IDE
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pages.login_page import LoginPage

# ---------------------------------------------------------------------------
# Test Data & Expected Messages
# ---------------------------------------------------------------------------
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
LOCKED_OUT_USER = "locked_out_user"
INVALID_USER = "invalid_user"
INVALID_PASSWORD = "wrong_password"

LOCKED_OUT_ERROR = "Epic sadface: Sorry, this user has been locked out."
USERNAME_REQUIRED_ERROR = "Epic sadface: Username is required"
PASSWORD_REQUIRED_ERROR = "Epic sadface: Password is required"
INVALID_CREDENTIALS_ERROR = (
    "Epic sadface: Username and password do not match any user in this service"
)


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------

@pytest.mark.auth
@pytest.mark.smoke
def test_tc_auth_001_successful_login(page: Page, login_page: LoginPage) -> None:
    """TC-AUTH-001: Successful Login with Standard User.

    Preconditions:
        User is navigated to the login page.
    Steps:
        1. Fill username with standard_user.
        2. Fill password with secret_sauce.
        3. Click login button.
    Expected:
        - Redirected to inventory page (https://www.saucedemo.com/inventory.html).
        - Header text displays 'Swag Labs'.
        - Inventory product list is visible.
    """
    # Action
    login_page.login(username=VALID_USERNAME, password=VALID_PASSWORD)

    # Assertion
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(login_page.app_logo).to_have_text("Swag Labs")
    expect(login_page.inventory_list).to_be_visible()


@pytest.mark.auth
@pytest.mark.negative
def test_tc_auth_002_locked_out_user(login_page: LoginPage) -> None:
    """TC-AUTH-002: Login Attempt with Locked-Out User.

    Preconditions:
        User is navigated to the login page.
    Steps:
        1. Fill username with locked_out_user.
        2. Fill password with secret_sauce.
        3. Click login button.
    Expected:
        - Error banner is displayed.
        - Error message contains lockout notice.
    """
    # Action
    login_page.login(username=LOCKED_OUT_USER, password=VALID_PASSWORD)

    # Assertion
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text(LOCKED_OUT_ERROR)


@pytest.mark.auth
@pytest.mark.negative
def test_tc_auth_003_empty_username(login_page: LoginPage) -> None:
    """TC-AUTH-003: Login Attempt with Empty Username.

    Preconditions:
        User is navigated to the login page.
    Steps:
        1. Leave username field empty.
        2. Fill password with secret_sauce.
        3. Click login button.
    Expected:
        - Error banner is displayed.
        - Error message states username is required.
    """
    # Act
    login_page.login(username="", password=VALID_PASSWORD)

    # Assert
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text(USERNAME_REQUIRED_ERROR)


@pytest.mark.auth
@pytest.mark.negative
def test_tc_auth_004_empty_password(login_page: LoginPage) -> None:
    """TC-AUTH-004: Login Attempt with Empty Password.

    Preconditions:
        User is navigated to the login page.
    Steps:
        1. Fill username with standard_user.
        2. Leave password field empty.
        3. Click login button.
    Expected:
        - Error banner is displayed.
        - Error message states password is required.
    """
    # Act
    login_page.login(username=VALID_USERNAME, password="")

    # Assert
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text(PASSWORD_REQUIRED_ERROR)


@pytest.mark.auth
@pytest.mark.negative
def test_tc_auth_005_invalid_credentials(login_page: LoginPage) -> None:
    """TC-AUTH-005: Login Attempt with Invalid Credentials.

    Preconditions:
        User is navigated to the login page.
    Steps:
        1. Fill username with invalid_user.
        2. Fill password with wrong_password.
        3. Click login button.
    Expected:
        - Error banner is displayed.
        - Error message states username and password do not match.
    """
    # Act
    login_page.login(username=INVALID_USER, password=INVALID_PASSWORD)

    # Assert
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text(INVALID_CREDENTIALS_ERROR)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

