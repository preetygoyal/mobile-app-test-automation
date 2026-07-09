"""Base class every screen object inherits from.

Locators throughout this project use Appium's accessibility-id strategy,
which matches the `content-desc` values baked into the demo app itself
(saucelabs/my-demo-app-rn) -- these are the same identifiers the app's own
official WebdriverIO/Mocha test suite uses, ported here to Python/pytest.
"""
from __future__ import annotations

import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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

    def _swipe_within(self, container_id: str, direction: str = "up"):
        """Swipes inside `container_id`'s bounds, using Appium's built-in
        UiAutomator2 gesture command."""
        container = self.find(container_id)
        rect = container.rect
        self.driver.execute_script(
            "mobile: swipeGesture",
            {
                "left": rect["x"],
                "top": rect["y"],
                "width": rect["width"],
                "height": rect["height"],
                "direction": direction,
                "percent": 0.75,
            },
        )

    def scroll_to(self, accessibility_id: str, container_id: str, max_scrolls: int = 6):
        """Repeatedly swipes inside `container_id` until the element identified
        by `accessibility_id` is on screen, then returns it.

        This mirrors `findElementBySwipe` in the demo app's own official test
        suite (__tests__/e2e/helpers/gestures.ts) -- several screens in this
        app (product details, the cart, and the lower items in the menu
        drawer) render content below the fold that has to be scrolled into
        view before Appium can find or click it. Clicking these elements
        without scrolling first was the actual cause of most CI test
        failures (Appium reporting "element not found" even though the
        element genuinely exists, just off-screen).
        """
        for _ in range(max_scrolls):
            if self.is_displayed(accessibility_id, timeout=2):
                return self.find(accessibility_id, timeout=2)
            try:
                self._swipe_within(container_id)
            except (TimeoutException, NoSuchElementException):
                break
        # Final attempt -- let the natural TimeoutException surface if the
        # element genuinely isn't there, rather than swallowing the error.
        return self.find(accessibility_id)

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
