"""Base class every screen object inherits from.

This project targets `appium/android-apidemos` (io.appium.android.apis), a
plain native Android app -- unlike a React Native app, its elements expose
normal Android resource-ids (e.g. `io.appium.android.apis:id/edit`) and
standard framework ids (e.g. `android:id/button1`), so locators here use
whichever Appium `By` strategy fits each element instead of assuming
everything has an accessibility id.
"""
from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 15


class BaseScreen:
    def __init__(self, driver):
        self.driver = driver

    def find(self, by: str, value: str, timeout: int = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(by, value)
        )

    def find_all(self, by: str, value: str):
        return self.driver.find_elements(by, value)

    def is_displayed(self, by: str, value: str, timeout: int = 5) -> bool:
        try:
            return self.find(by, value, timeout=timeout).is_displayed()
        except TimeoutException:
            return False

    def scroll_to_text(self, text: str, timeout: int = DEFAULT_TIMEOUT):
        """Scrolls the nearest scrollable container until an element with
        this exact visible text is on screen, then returns it.

        Uses UiAutomator2's built-in `UiScrollable.scrollTextIntoView`
        instead of manually computing swipe gestures: UiAutomator itself
        knows the list's real scroll state, so this is far more reliable
        than guessing swipe distances/counts (the approach the previous
        app in this repo needed, and which was a repeated source of
        flakiness).
        """
        selector = (
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollTextIntoView("{text}")'
        )
        return self.find(AppiumBy.ANDROID_UIAUTOMATOR, selector, timeout=timeout)
