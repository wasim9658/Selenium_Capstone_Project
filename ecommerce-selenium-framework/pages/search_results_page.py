from typing import List

from selenium.webdriver.common.by import By

from pages.base_page import BasePage, xpath_literal


class SearchResultsPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "#content h1")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "div.product-layout h4 a")

    def heading(self) -> str:
        return self.text_of(self.HEADING)

    def product_names(self) -> List[str]:
        self.visible(self.HEADING)
        return [el.text.strip() for el in self.driver.find_elements(*self.PRODUCT_NAMES)]

    def add_to_cart(self, product_name: str) -> str:
        """Click 'Add to Cart' on the card whose title is exactly `product_name`.

        Returns the success banner text. Any native JS alert raised meanwhile is handled.
        """
        card_button = (
            By.XPATH,
            "//div[contains(@class,'product-layout')]"
            f"[.//h4/a[normalize-space()={xpath_literal(product_name)}]]"
            "//button[contains(@onclick,'cart.add')]",
        )
        self.click(card_button)
        self.handle_alert_if_present(timeout=1)
        return self.success_message()
