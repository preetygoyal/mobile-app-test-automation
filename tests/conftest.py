"""
Appium session management for the demo app (saucelabs/my-demo-app-rn).

The app has its own built-in "reset" gesture instead of needing a fresh
install between tests: long-pressing the header logo clears in-app state
(cart contents, login session). We replicate that here via `reset_app_state`,
which runs automatically before every test -- this mirrors exactly how the
app's own official test suite resets between scenarios.

IMPORTANT: the official suite's `restartApp()` helper
(saucelabs/my-demo-app-rn __tests__/e2e/helpers/utils.ts) does two things,
not one: it calls `driver.reset()` (a full terminate+relaunch of the app)
for every test *except* the first, and only *then* does the long-press
gesture. Earlier revisions of this fixture did the long-press alone. That
works for the very first test (the app is still sitting on its initial
cold-launch route), but once a test navigates away from the Catalog screen
(e.g. to Cart), the long-press alone does not reliably bring the app back
to a populated Catalog -- so every test after the first either raced an
empty product list (IndexError) or, after a wait was added here, timed out
waiting for a product list that was never coming back. Relaunching the app
first, exactly like the official helper, is what actually returns the app
to the Catalog screen every time.
"""
from __future__ import annotations

import os

import pytest
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from pages.cart_screen import CartScreen
from pages.catalog_screen import CatalogScreen
from pages.item_details_screen import ItemDetailsScreen
from pages.login_screen import LoginScreen
from pages.menu_screen import MenuScreen
from pages.sort_modal import SortModal

APP_PACKAGE = "com.saucelabs.mydemoapp.rn"
APP_ACTIVITY = ".MainActivity"
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://localhost:4723")
APK_PATH = os.getenv("APK_PATH", os.path.join(os.path.dirname(__file__), "..", "app", "MyDemoAppRN.apk"))
PLATFORM_VERSION = os.getenv("PLATFORM_VERSION", "13")
DEVICE_NAME = os.getenv("DEVICE_NAME", "Android Emulator")

RESET_APP_ACCESSIBILITY_ID = "longpress reset app"


@pytest.fixture(scope="session")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = DEVICE_NAME
    options.platform_version = PLATFORM_VERSION
    options.app = os.path.abspath(APK_PATH)
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = False
    options.new_command_timeout = 120

    appium_driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
    yield appium_driver
    appium_driver.quit()


_first_test_done = False


@pytest.fixture(autouse=True)
def reset_app_state(driver):
    """Restarts the app and long-presses the header logo to reset cart/login
    state, exactly like the app's own test harness does between scenarios
    (see the module docstring above for why both steps are needed).
    """
    global _first_test_done
    if _first_test_done:
        # Full terminate + relaunch, matching the official suite's
        # `driver.reset()` call. This is what actually returns the app to
        # the Catalog screen; the long-press alone does not, once a
        # previous test has navigated elsewhere.
        driver.terminate_app(APP_PACKAGE)
        driver.activate_app(APP_PACKAGE)
    _first_test_done = True

    # 60s (not 15s): on a cold/un-cached emulator boot (no AVD snapshot to
    # restore from -- e.g. the first run after the actions/cache key
    # changes), the Android activity reports "started" well before the
    # React Native JS bundle has actually finished initializing and
    # rendering the first screen under CI's software-rendered GPU
    # (swiftshader). A run was observed where this find never succeeded
    # within 15s for the *entire* session even though the same app rendered
    # in under a second once warmed up in a cache-hit run. A longer ceiling
    # costs nothing on fast runs (WebDriverWait returns as soon as the
    # element appears) but tolerates a slow cold start / relaunch.
    header = WebDriverWait(driver, 60).until(
        lambda d: d.find_element(AppiumBy.ACCESSIBILITY_ID, RESET_APP_ACCESSIBILITY_ID)
    )
    driver.execute_script("mobile: longClickGesture", {"elementId": header.id, "duration": 1000})
    WebDriverWait(driver, 30).until(
        lambda d: len(d.find_elements(AppiumBy.ACCESSIBILITY_ID, "store item")) > 0
    )
    yield


@pytest.fixture
def login_screen(driver):
    return LoginScreen(driver)


@pytest.fixture
def menu_screen(driver):
    return MenuScreen(driver)


@pytest.fixture
def catalog_screen(driver):
    return CatalogScreen(driver)


@pytest.fixture
def item_details_screen(driver):
    return ItemDetailsScreen(driver)


@pytest.fixture
def cart_screen(driver):
    return CartScreen(driver)


@pytest.fixture
def sort_modal(driver):
    return SortModal(driver)
