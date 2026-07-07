"""Base class every screen object inherits from.

Locators throughout this project use Appium's accessibility-id strategy,
which matches the `content-desc` values baked into the demo app itself
(saucelabs/my-demo-app-rn) -- these are the same identifiers the app's own
official WebdriverIO/Mocha test suite uses, ported here to Python/pytest.
"""
from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 15


class BaseScreen:
    def __init__(self, driver):
        self.driver = driver

    def find(self, accessibility_id: str, timeout: int = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(AppiumBy.ACCESSIBILITY_ID, accessibility_id)
        )

    def find_all(self, accessibility_id: str):
        return self.driver.find_elements(AppiumBy.ACCESSIBILITY_ID, accessibility_id)

    def find_by_xpath(self, xpath: str, timeout: int = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(AppiumBy.XPATH, xpath)
        )

    def is_displayed(self, accessibility_id: str, timeout: int = 5) -> bool:
        try:
            return self.find(accessibility_id, timeout=timeout).is_displayed()
        except TimeoutException:
            return False

    def long_press(self, element, duration_ms: int = 1000):
        """Long-press gesture, used by the demo app to reset its own state
        (matches the app's own restartApp() helper, which long-presses the
        header logo rather than reinstalling the app between tests)."""
        self.driver.execute_script(
            "mobile: longClickGesture",
            {"elementId": element.id, "duration": duration_ms},
        )

    def get_visible_text(self, element) -> str:
        """Android often doesn't expose text on a container element directly --
        the app's own test suite works around this by concatenating the text
        of every child TextView instead. This mirrors that approach."""
        try:
            text_views = element.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
            combined = " ".join(tv.text for tv in text_views if tv.text)
            return combined.strip() or element.text.strip()
        except Exception:
            return element.text.strip()
