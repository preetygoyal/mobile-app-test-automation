from .base_screen import BaseScreen


class SortModal(BaseScreen):
    NAME_ASC = "nameAsc"
    NAME_DESC = "nameDesc"
    PRICE_ASC = "priceAsc"
    PRICE_DESC = "priceDesc"

    def sort_name_asc(self):
        self.find(self.NAME_ASC).click()

    def sort_name_desc(self):
        self.find(self.NAME_DESC).click()

    def sort_price_asc(self):
        self.find(self.PRICE_ASC).click()

    def sort_price_desc(self):
        self.find(self.PRICE_DESC).click()

    def get_active_option_text(self) -> str:
        xpath = '//android.view.ViewGroup[@content-desc="active option"]/../android.widget.TextView'
        return self.find_by_xpath(xpath).text
