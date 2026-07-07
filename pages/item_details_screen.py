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
        self.find(self.ADD_TO_CART_BUTTON).click()

    def increase_quantity(self):
        self.find(self.COUNTER_PLUS).click()

    def decrease_quantity(self):
        self.find(self.COUNTER_MINUS).click()

    def get_quantity(self) -> int:
        return int(self.find(self.COUNTER_AMOUNT).text)

    def go_back(self):
        self.driver.back()
