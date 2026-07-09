from appium.webdriver.common.appiumby import AppiumBy

from .base_screen import BaseScreen


class HomeScreen(BaseScreen):
    """The app's root screen: a drill-down category list (ApiDemos.java
    groups every sample activity by splitting its label on '/', so e.g.
    'App/Alert Dialogs' becomes a two-step tap: 'App' then 'Alert
    Dialogs'). Rows render as plain `android.widget.TextView` via the
    stock `android.R.layout.simple_list_item_1`, and the list container
    itself is the standard `android:id/list`.
    """

    LIST_CONTAINER = (AppiumBy.ID, "android:id/list")

    def is_shown(self) -> bool:
        return self.is_displayed(*self.LIST_CONTAINER, timeout=10)

    def open_category(self, name: str):
        """Taps a single category/leaf row by its exact visible label,
        scrolling it into view first if it's off screen."""
        self.scroll_to_text(name).click()

    def open(self, *path: str):
        """Drills into a '/'-separated path one tap at a time, e.g.
        `open("App", "Alert Dialogs")`."""
        for step in path:
            self.open_category(step)
