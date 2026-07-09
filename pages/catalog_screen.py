from appium.webdriver.common.appiumby import AppiumBy

from .base_screen import BaseScreen


class CatalogScreen(BaseScreen):
    PRODUCTS_SCREEN = "products screen"
    STORE_ITEM = "store item"
    SORT_BUTTON = "sort button"

    def is_shown(self) -> bool:
        return self.is_displayed(self.PRODUCTS_SCREEN, timeout=10)

    def items(self):
        return self.find_all(self.STORE_ITEM)

    def items_count(self) -> int:
        return len(self.items())

    def get_item_name(self, index: int) -> str:
        return self.get_visible_text(self.items()[index])

    def open_sort_modal(self):
        self.find(self.SORT_BUTTON).click()

    def open_item_by_name(self, name: str):
        xpath = (
            f"//android.widget.TextView[contains(@text,'{name}')]"
            "/ancestor::*[@content-desc='store item']"
        )
        # Items further down the catalog list can be below the fold, so
        # scroll the products screen until the matching item is visible
        # before clicking (mirrors the app's own official test suite,
        # which always scroll-to-find catalog items rather than assuming
        # they're already on screen).
        for _ in range(6):
            try:
                element = self.driver.find_element("xpath", xpath)
                if element.is_displayed():
                    element.click()
                    return
            except Exception:
                pass
            try:
                self._swipe_within(self.PRODUCTS_SCREEN)
            except Exception:
                break
        self.find_by_xpath(xpath).click()
