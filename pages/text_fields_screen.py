from appium.webdriver.common.appiumby import AppiumBy

from .base_screen import BaseScreen


class TextFieldsScreen(BaseScreen):
    """Views/TextFields (io.appium.android.apis.view.TextFields).

    Only the topmost EditText (resource-id `edit`) is used here; it has no
    content-desc, just a "hint text" hint and no special input type.
    """

    FIRST_FIELD = (AppiumBy.ID, "io.appium.android.apis:id/edit")

    def is_shown(self) -> bool:
        return self.is_displayed(*self.FIRST_FIELD, timeout=10)

    def enter_text(self, text: str):
        field = self.find(*self.FIRST_FIELD)
        field.clear()
        if text:
            field.send_keys(text)

    def get_text(self) -> str:
        return self.find(*self.FIRST_FIELD).text
