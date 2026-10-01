"""End-to-end purchase journey on the TutorialsNinja (OpenCart) demo store.

Steps covered
  1 Launch browser            (driver fixture)
  2 Login                     (registered_user fixture creates the account first)
  3 Search product            (Excel: Search Term)
  4 Add product to cart       (Excel: Product Name)
  5 Update quantity           (Excel: Update Quantity)
  6 Verify cart details
  7 Capture screenshots       (snap fixture, one per step)
  8 Test data from Excel/JSON (products.xlsx + test_data.json)
  9 Handle popups/alerts      (BasePage.handle_alert_if_present / close_banners)
 10 Execution report          (reports/execution_report.html)
"""
from decimal import Decimal

import pytest

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.data_reader import read_excel_rows
from utils.logger import get_logger

log = get_logger("tests")

PRODUCTS = read_excel_rows()  # rows with Run = N are already filtered out
PRICE_TOLERANCE = Decimal("0.05")  # store rounds tax to 2 decimals


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize("data", PRODUCTS, ids=[row["TestCase ID"] for row in PRODUCTS])
def test_purchase_flow(driver, config, snap, registered_user, data):
    base, wait = config["base_url"], config["explicit_wait"]
    product = data["Product Name"]
    new_qty = int(data["Update Quantity"])

    # ---- Step 1: launch browser & open the store ---------------------------
    home = HomePage(driver, base, wait).load()
    assert "Your Store" in home.title(), f"Unexpected home page title: {home.title()!r}"
    snap("01_home_page")

    # ---- Step 2: login ------------------------------------------------------
    login = LoginPage(driver, base, wait).load()
    login.login(registered_user["email"], registered_user["password"])
    assert login.is_logged_in(), "Login failed - 'My Account' page was not displayed"
    log.info("Logged in as %s", registered_user["email"])
    snap("02_logged_in")

    # ---- Step 3: search the product ----------------------------------------
    home = HomePage(driver, base, wait).load()
    results = home.search(data["Search Term"])
    names = results.product_names()
    log.info("Search %r returned: %s", data["Search Term"], names)
    assert product in names, f"{product!r} not found in search results {names}"
    snap("03_search_results")

    # ---- Step 4: add to cart (also handles any JS alert) --------------------
    message = results.add_to_cart(product)
    assert product in message and "added" in message.lower(), f"Unexpected message: {message!r}"
    snap("04_added_to_cart")
    results.close_banners()  # popup handling: dismiss the HTML success banner

    # ---- Step 5: update quantity on the cart page ---------------------------
    cart = CartPage(driver, base, wait).load()
    assert cart.is_product_in_cart(product), f"{product!r} missing from cart"
    assert cart.get_quantity(product) == 1, "Newly added product should start with quantity 1"
    snap("05_cart_before_update")

    update_msg = cart.update_quantity(product, new_qty)
    assert "modified" in update_msg.lower(), f"Cart update not confirmed: {update_msg!r}"
    snap("06_cart_after_update")

    # ---- Step 6: verify cart details ---------------------------------------
    assert cart.is_product_in_cart(product)
    assert cart.get_quantity(product) == new_qty

    unit = cart.get_unit_price(product)
    line_total = cart.get_line_total(product)
    grand_total = cart.get_grand_total()
    log.info("Cart: %s x%s @ %s = %s (grand total %s)", product, new_qty, unit, line_total, grand_total)

    assert abs(line_total - unit * new_qty) <= PRICE_TOLERANCE, (
        f"Line total {line_total} != unit price {unit} x qty {new_qty}")
    assert grand_total > 0, "Cart grand total should be greater than zero"

    header_count = HomePage(driver, base, wait).header_cart_item_count()
    assert header_count == new_qty, f"Header mini-cart shows {header_count} item(s), expected {new_qty}"
    snap("07_cart_verified")


@pytest.mark.regression
def test_login_with_invalid_credentials_shows_error(driver, config, test_data, snap):
    """Negative scenario driven from test_data.json."""
    neg = test_data["negative_login"]
    login = LoginPage(driver, config["base_url"], config["explicit_wait"]).load()
    login.login(neg["email"], neg["password"])

    assert neg["expected_error"] in login.error_message()
    assert not login.is_logged_in(timeout=1)
    snap("invalid_login_error")
