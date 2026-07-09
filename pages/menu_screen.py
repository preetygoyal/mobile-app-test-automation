import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from .base_screen import BaseScreen

ANDROID_LOG_OUT_BUTTON = "//android.widget.Button[contains(@text,'LOG OUT')]"
ANDROID_OK_BUTTON = "//android.widget.Button[contains(@text,'OK')]"


class MenuScreen(BaseScreen):
    OPEN_MENU_BUTTON = "open menu"
    CLOSE_MENU_BUTTON = "close menu"
    CATALOG_ITEM = "menu item catalog"
    LOGIN_ITEM = "menu item log in"
    LOGOUT_ITEM = "menu item log out"

    def open_menu(self):
        self.find(self.OPEN_MENU_BUTTON).click()
        # Wait for the drawer's open animation to finish.
        time.sleep(1)

    def close_menu(self):
        self.find(self.CLOSE_MENU_BUTTON).click()
        time.sleep(0.75)

    def open_login(self):
        # Log in / Log out sit near the bottom of the menu drawer, below
        # several other items -- the app's own official test suite always
        # scrolls the drawer (using the always-visible "menu item catalog"
        # entry as the scrollable reference) before clicking these.
        self.scroll_to(self.LOGIN_ITEM, self.CATALOG_ITEM).click()

    # timeout=8, not 3: checked right after login/logout completes, and a
    # run was observed where the drawer item's label hadn't finished
    # re-rendering ("log out" -> "log in" or vice versa) within 3s under
    # CI's slower emulator, producing a false read of the *previous* state.
    def is_logged_in(self) -> bool:
        return self.is_displayed(self.LOGOUT_ITEM, timeout=8)

    def logout(self):
        """Mirrors the app's own logout flow: tapping the menu item pops up a
        native confirmation dialog with LOG OUT / CANCEL, then an OK toast."""
        self.scroll_to(self.LOGOUT_ITEM, self.CATALOG_ITEM).click()
        log_out_button = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(AppiumBy.XPATH, ANDROID_LOG_OUT_BUTTON)
        )
        log_out_button.click()
        ok_button = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(AppiumBy.XPATH, ANDROID_OK_BUTTON)
        )
        ok_button.click()
        time.sleep(1)
