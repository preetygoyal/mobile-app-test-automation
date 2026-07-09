from appium.webdriver.common.appiumby import AppiumBy

from .base_screen import BaseScreen


class AlertDialogScreen(BaseScreen):
    """App/Alert Dialogs (io.appium.android.apis.app.AlertDialogSamples).

    Only the simple "OK Cancel dialog with a message" trigger is used here
    (button id `two_buttons`); the resulting AlertDialog's buttons use the
    standard AOSP AlertDialog ids (`android:id/button1` = positive/OK,
    `android:id/button2` = negative/Cancel), which are framework ids, not
    specific to this app.
    """

    TWO_BUTTONS_TRIGGER = (AppiumBy.ID, "io.appium.android.apis:id/two_buttons")
    DIALOG_TITLE = (AppiumBy.ID, "android:id/alertTitle")
    OK_BUTTON = (AppiumBy.ID, "android:id/button1")
    CANCEL_BUTTON = (AppiumBy.ID, "android:id/button2")

    def is_shown(self) -> bool:
        return self.is_displayed(*self.TWO_BUTTONS_TRIGGER, timeout=10)

    def open_two_buttons_dialog(self):
        self.find(*self.TWO_BUTTONS_TRIGGER).click()

    def is_dialog_shown(self) -> bool:
        return self.is_displayed(*self.DIALOG_TITLE, timeout=5)

    def tap_ok(self):
        self.find(*self.OK_BUTTON).click()

    def tap_cancel(self):
        self.find(*self.CANCEL_BUTTON).click()
