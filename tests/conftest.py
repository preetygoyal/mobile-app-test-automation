"""
Appium session management for the demo app (saucelabs/my-demo-app-rn).

The app has its own built-in "reset" gesture instead of needing a fresh
install between tests: long-pressing the header logo clears in-app state
(cart contents, login session). We replicate that here via `reset_app_state`,
which runs automatically before every test -- this mirrors exactly how the
app's own official test suite resets between scenarios.
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


@pytest.fixture(autouse=True)
def reset_app_state(driver):
    """Long-presses the header logo to reset cart/login state, exactly like
    the app's own test harness does between scenarios.

    The reset gesture triggers an async reload of the catalog screen. Screen
    objects that read the product list without an explicit wait (e.g.
    `CatalogScreen.items()` -> `BaseScreen.find_all()`, which calls
    `driver.find_elements()` with no polling) were racing that reload: right
    after the long-press, the list is often still empty, so `items()[0]`
    raised `IndexError: list index out of range` and login tests (which
    depend on the same app-bar "open menu" button rendering) timed out with
    NoSuchElementError. Waiting here for at least one product to reappear
    ensures every test starts from a screen that has actually finished
    reloading, instead of an empty one mid-reload.
    """
    # 60s (not 15s): on a cold/un-cached emulator boot (no AVD snapshot to
    # restore from -- e.g. the first run after the actions/cache key
    # changes), the Android activity reports "started" well before the
    # React Native JS bundle has actually finished initializing and
    # rendering the first screen under CI's software-rendered GPU
    # (swiftshader). A run was observed where this find never succeeded
    # within 15s for the *entire* session (all 15 tests errored in fixture
    # setup) even though the same app rendered in under a second once
    # warmed up in a cache-hit run. A longer ceiling costs nothing on fast
    # runs (WebDriverWait returns as soon as the element appears) but
    # tolerates a slow cold start instead of failing the whole suite.
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
