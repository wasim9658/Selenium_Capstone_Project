import re
from decimal import Decimal

from selenium.webdriver.common.by import By

from pages.base_page import BasePage, xpath_literal


def to_decimal(price_text: str) -> Decimal:
    """'$1,806.00' -> Decimal('1806.00')"""
    cleaned = re.sub(r"[^\d.]", "", price_text)
    return Decimal(cleaned)


class CartPage(BasePage):
    GRAND_TOTAL = (
        By.XPATH,
        "//div[@id='content']//strong[normalize-space()='Total:']/ancestor::tr[1]/td[last()]",
    )

    def load(self) -> "CartPage":
        self.open_route("checkout/cart")
        return self

    # -------------------------------------------------------------- locators
    @staticmethod
    def _row(product_name: str) -> tuple:
        return (
            By.XPATH,
            "//div[@id='content']//form//tbody/tr"
            f"[.//td/a[normalize-space()={xpath_literal(product_name)}]]",
        )

    def _in_row(self, product_name: str, xpath: str) -> tuple:
        by, row_xpath = self._row(product_name)
        return by, row_xpath + xpath

    # ---------------------------------------------------------------- reading
    def is_product_in_cart(self, product_name: str) -> bool:
        return self.is_present(self._row(product_name), timeout=5)

    def get_quantity(self, product_name: str) -> int:
        box = self.visible(self._in_row(product_name, "//input[starts-with(@name,'quantity')]"))
        return int(box.get_attribute("value"))

    def get_unit_price(self, product_name: str) -> Decimal:
        return to_decimal(self.text_of(self._in_row(product_name, "//td[@class='text-right'][1]")))

    def get_line_total(self, product_name: str) -> Decimal:
        return to_decimal(self.text_of(self._in_row(product_name, "//td[@class='text-right'][2]")))

    def get_grand_total(self) -> Decimal:
        return to_decimal(self.text_of(self.GRAND_TOTAL))

    # ----------------------------------------------------------------- update
    def update_quantity(self, product_name: str, quantity: int) -> str:
        """Change the quantity box, press the Update button, return the success message."""
        self.type(self._in_row(product_name, "//input[starts-with(@name,'quantity')]"), quantity)
        # In the row, the Update button is type=submit; the Remove button is type=button.
        self.click(self._in_row(product_name, "//button[@type='submit']"))
        self.handle_alert_if_present(timeout=1)
        return self.success_message()
