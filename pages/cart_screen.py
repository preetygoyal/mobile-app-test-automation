import time

from .base_screen import BaseScreen


class CartScreen(BaseScreen):
    CART_SCREEN = "cart screen"
    CART_BADGE = "cart badge"
    PRODUCT_ROW = "product row"
    GO_SHOPPING_BUTTON = "Go Shopping button"
    PROCEED_TO_CHECKOUT_BUTTON = "Proceed To Checkout button"
    CHECKOUT_FOOTER = "checkout footer"

    def open_cart(self):
        self.find(self.CART_BADGE).click()

    def is_shown(self) -> bool:
        return self.is_displayed(self.CART_SCREEN, timeout=10)

    def items_count(self) -> int:
        return len(self.find_all(self.PRODUCT_ROW))

    def go_shopping(self):
        self.find(self.GO_SHOPPING_BUTTON).click()

    def proceed_to_checkout_visible(self) -> bool:
        return self.is_displayed(self.PROCEED_TO_CHECKOUT_BUTTON, timeout=5)

    def proceed_to_checkout(self):
        self.find(self.PROCEED_TO_CHECKOUT_BUTTON).click()

    def get_checkout_footer_text(self) -> str:
        return self.find(self.CHECKOUT_FOOTER).text

    def remove_item(self, name: str):
        """Removes the first cart row whose visible text contains `name`."""
        xpath = (
            f"//android.widget.TextView[contains(@text,'{name}')]"
            "/ancestor::*[@content-desc='product row']"
        )
        # Scroll the cart screen until the matching row is visible, same
        # reasoning as CatalogScreen.open_item_by_name.
        row = None
        for _ in range(6):
            try:
                candidate = self.driver.find_element("xpath", xpath)
                if candidate.is_displayed():
                    row = candidate
                    break
            except Exception:
                pass
            try:
                self._swipe_within(self.CART_SCREEN)
            except Exception:
                break
        if row is None:
            row = self.find_by_xpath(xpath)
        row.find_element("accessibility id", "remove item").click()
        # Let the cart's internal state finish updating.
        time.sleep(1)
