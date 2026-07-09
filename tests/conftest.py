"""
Appium session management for the demo app (appium/android-apidemos).

This app has no login/cart state, so unlike the previous app this repo
tested, there's no custom in-app "reset" gesture involved -- the fixture
just terminates and relaunches the app before every test. That turned out
to be the reliable pattern in this repo's own history too: an earlier
attempt at a lighter-weight "long-press to reset" gesture (against a
different, stateful app) repeatedly failed to reliably return to a known
screen once a test had navigated elsewhere, and a full relaunch was what
actually fixed it. Starting from that lesson here avoids repeating it.
"""
from __future__ import annotations

import os

import pytest
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from pages.alert_dialog_screen import AlertDialogScreen
from pages.home_screen import HomeScreen
from pages.text_fields_screen import TextFieldsScreen

APP_PACKAGE = "io.appium.android.apis"
APP_ACTIVITY = ".ApiDemos"
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://localhost:4723")
APK_PATH = os.getenv("APK_PATH", os.path.join(os.path.dirname(__file__), "..", "app", "ApiDemos-debug.apk"))
PLATFORM_VERSION = os.getenv("PLATFORM_VERSION", "11")
DEVICE_NAME = os.getenv("DEVICE_NAME", "Android Emulator")


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
    """Relaunches the app fresh before every test so each one starts from
    the same known screen (the home category list), regardless of which
    screen or open dialog the previous test left behind.

    60s (not the framework default) for the post-relaunch wait: on a
    cold/un-cached emulator boot the app's first render can take
    noticeably longer than on a warm one -- see this repo's git history
    for a run where a tighter timeout here caused spurious failures on a
    slow CI boot even though the app was working fine.
    """
    driver.terminate_app(APP_PACKAGE)
    driver.activate_app(APP_PACKAGE)
    WebDriverWait(driver, 60).until(
        lambda d: d.find_element(AppiumBy.ID, "android:id/list")
    )
    yield


@pytest.fixture
def home_screen(driver):
    return HomeScreen(driver)


@pytest.fixture
def alert_dialog_screen(driver):
    return AlertDialogScreen(driver)


@pytest.fixture
def text_fields_screen(driver):
    return TextFieldsScreen(driver)
