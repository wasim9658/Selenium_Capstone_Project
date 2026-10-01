import re

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage


class HomePage(BasePage):
    SEARCH_BOX = (By.NAME, "search")
    SEARCH_BTN = (By.CSS_SELECTOR, "#search button")
    CART_TOTAL = (By.ID, "cart-total")

    def load(self) -> "HomePage":
        self.open(self.base_url)
        return self

    def title(self) -> str:
        return self.driver.title

    def search(self, term: str) -> SearchResultsPage:
        self.type(self.SEARCH_BOX, term)
        self.click(self.SEARCH_BTN)
        return SearchResultsPage(self.driver, self.base_url, self.timeout)

    def header_cart_item_count(self) -> int:
        """Header mini-cart reads like '3 item(s) - $1,806.00'."""
        text = self.text_of(self.CART_TOTAL)
        match = re.search(r"(\d+)\s+item", text)
        return int(match.group(1)) if match else 0
