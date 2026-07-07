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

    def close_menu(self):
        self.find(self.CLOSE_MENU_BUTTON).click()

    def open_login(self):
        self.find(self.LOGIN_ITEM).click()

    def is_logged_in(self) -> bool:
        return self.is_displayed(self.LOGOUT_ITEM, timeout=3)

    def logout(self):
        """Mirrors the app's own logout flow: tapping the menu item pops up a
        native confirmation dialog with LOG OUT / CANCEL, then an OK toast."""
        self.find(self.LOGOUT_ITEM).click()
        log_out_button = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(AppiumBy.XPATH, ANDROID_LOG_OUT_BUTTON)
        )
        log_out_button.click()
        ok_button = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(AppiumBy.XPATH, ANDROID_OK_BUTTON)
        )
        ok_button.click()
