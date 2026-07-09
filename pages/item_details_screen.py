import time

from .base_screen import BaseScreen


class ItemDetailsScreen(BaseScreen):
    PRODUCT_SCREEN = "product screen"
    CONTAINER_HEADER = "container header"
    BACK_BUTTON = "navigation back button"
    ADD_TO_CART_BUTTON = "Add To Cart button"
    COUNTER_MINUS = "counter minus button"
    COUNTER_AMOUNT = "counter amount"
    COUNTER_PLUS = "counter plus button"

    def is_shown(self) -> bool:
        return self.is_displayed(self.PRODUCT_SCREEN, timeout=10)

    def product_name(self) -> str:
        return self.find(self.CONTAINER_HEADER).text

    def add_to_cart(self):
        # The Add To Cart button sits below the fold on most product pages
        # and needs to be scrolled into view first (see BaseScreen.scroll_to).
        self.scroll_to(self.ADD_TO_CART_BUTTON, self.PRODUCT_SCREEN).click()
        # Let the app's internal cart state finish updating before the next
        # screen interaction (matches the official screen object's own pause).
        time.sleep(1)

    def increase_quantity(self):
        self.scroll_to(self.COUNTER_PLUS, self.PRODUCT_SCREEN).click()
        time.sleep(1)

    def decrease_quantity(self):
        self.scroll_to(self.COUNTER_MINUS, self.PRODUCT_SCREEN).click()
        time.sleep(1)

    def get_quantity(self) -> int:
        return int(self.find(self.COUNTER_AMOUNT).text)

    def go_back(self):
        self.driver.back()
