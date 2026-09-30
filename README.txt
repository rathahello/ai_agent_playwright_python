===============================================================================
SauceDemo Test Automation Suite (Playwright + Python)
===============================================================================

Automated End-to-End (E2E) testing framework for SauceDemo (https://www.saucedemo.com/)
built with Python, Playwright, and Pytest, implementing the Page Object Model (POM)
design pattern.

-------------------------------------------------------------------------------
1. PROJECT STRUCTURE
-------------------------------------------------------------------------------

SauceDemo_system-playwright-python/
│
├── pages/                   # Page Object Model classes
│   ├── base_page.py         # Base page with common navigation and utilities
│   ├── login_page.py        # SauceDemo Login page locators and actions
│   ├── inventory_page.py    # Products / Inventory page object
│   ├── cart_page.py         # Shopping cart page object
│   ├── checkout_page.py     # Checkout flow page object
│   └── navigation_page.py   # Sidebar menu navigation & session controls
│
├── tests/                   # Test suites organized by feature
│   ├── test_auth.py         # Authentication tests (TC-AUTH-001 to 005)
│   ├── test_cart.py         # Cart management tests (TC-CART-001 to 004)
│   ├── test_inventory.py    # Product inventory tests
│   ├── test_checkout.py     # Checkout process tests
│   └── test_navigation.py   # Menu navigation & state reset tests
│
├── reports/                 # Test execution outputs (ignored by git)
│   ├── report.html          # Interactive HTML test report
│   └── artifacts/           # Test videos (.webm) and screenshots (.png)
│
├── conftest.py              # Pytest fixtures and browser lifecycle hooks
├── pytest.ini               # Central Pytest configuration (options, markers, paths)
├── requirements.txt         # Project dependencies
└── README.txt               # Project documentation

-------------------------------------------------------------------------------
2. PREREQUISITES & INSTALLATION
-------------------------------------------------------------------------------

[Step 1] Python Version
Make sure Python 3.9+ is installed on your computer.

[Step 2] Setup Virtual Environment (Recommended)
Open PowerShell / Terminal in the project root:

  # Create virtual environment:
  python -m venv .venv

  # Activate on Windows (PowerShell):
  .venv\Scripts\Activate.ps1

  # Activate on macOS / Linux:
  source .venv/bin/activate

[Step 3] Install Dependencies
  pip install -r requirements.txt

[Step 4] Install Playwright Browsers
  playwright install

-------------------------------------------------------------------------------
3. HOW TO RUN TESTS
-------------------------------------------------------------------------------

All default settings (reporting, slow-motion, video, screenshots) are
automatically loaded from pytest.ini.

* Run all tests (headless / background):
  pytest

* Run all tests with browser UI visible (headed mode):
  pytest --headed

* Run a specific test file:
  pytest tests/test_auth.py
  pytest tests/test_cart.py

* Run tests by marker category:
  pytest -m smoke        # Run critical smoke tests
  pytest -m auth         # Run authentication suite
  pytest -m cart         # Run shopping cart suite
  pytest -m negative     # Run negative / validation error tests

* Run a specific test case:
  pytest -k test_tc_auth_001_successful_login

-------------------------------------------------------------------------------
4. VIEWING TEST REPORTS & EVIDENCE
-------------------------------------------------------------------------------

After tests run, all evidence is saved in the "reports/" folder:

1. Interactive HTML Report:
   Open "reports/report.html" in Chrome or Edge:

   - From Windows PowerShell:
     Start-Process .\reports\report.html

   - From Command Prompt:
     start .\reports\report.html

   - Or right-click "reports/report.html" in File Explorer and open with browser.

2. Video Recordings:
   Saved in: reports/artifacts/<test_name>/video.webm

3. Final State Screenshots:
   Saved in: reports/artifacts/<test_name>/test-finished-1.png

-------------------------------------------------------------------------------
5. CONFIGURATION DETAILS (pytest.ini)
-------------------------------------------------------------------------------

- pythonpath = .
  Resolves the root folder so imports like "from pages.login_page import LoginPage"
  work smoothly without errors.

- testpaths = tests
  Directs pytest to look for tests inside the "tests/" folder.

- --slowmo 500
  Adds a 500 millisecond (0.5 second) delay between actions so human eyes
  can observe the browser in headed mode.

- --html=reports/report.html --self-contained-html
  Generates a standalone, interactive HTML dashboard.

- --screenshot=on
  Takes a screenshot of the final page state for each test.

- --video=on
  Records a video of every test run in .webm format.

- --output=reports/artifacts
  Saves all video and screenshot files inside the "reports/artifacts" directory.

-------------------------------------------------------------------------------
6. ARCHITECTURE & CODING STANDARDS
-------------------------------------------------------------------------------

- Page Object Model (POM):
  Selectors and user interaction logic reside inside the "pages/" directory.
  Test files only call clean methods on page objects.

- AAA Pattern:
  All test functions follow the Arrange -> Action -> Assertion structure
  for maximum clarity and readability.

- Strict Type Hinting:
  All functions and fixtures specify parameter and return types (e.g., -> None).
===============================================================================
