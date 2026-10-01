"""BasePage: shared Selenium helpers used by every page object."""
from typing import Optional, Tuple

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import get_logger

Locator = Tuple[str, str]
log = get_logger("pages")


def xpath_literal(text: str) -> str:
    """Safely embed any string (including quotes) into an XPath expression."""
    if "'" not in text:
        return f"'{text}'"
    if '"' not in text:
        return f'"{text}"'
    parts = text.split("'")
    return "concat(" + ', "\'", '.join(f"'{p}'" for p in parts) + ")"


class BasePage:
    # Bootstrap "x" button on OpenCart alert banners
    ALERT_CLOSE_BTN: Locator = (By.CSS_SELECTOR, "div.alert button.close")
    SUCCESS_BANNER: Locator = (By.CSS_SELECTOR, "div.alert-success")
    DANGER_BANNER: Locator = (By.CSS_SELECTOR, "div.alert-danger")

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 15):
        self.driver = driver
        self.base_url = base_url if base_url.endswith("/") else base_url + "/"
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout, ignored_exceptions=(StaleElementReferenceException,))

    # ------------------------------------------------------------ navigation
    def open(self, url: str) -> None:
        log.info("Opening %s", url)
        self.driver.get(url)

    def open_route(self, route: str) -> None:
        self.open(f"{self.base_url}index.php?route={route}")

    # ---------------------------------------------------------------- finders
    def visible(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        w = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return w.until(EC.visibility_of_element_located(locator))

    def is_present(self, locator: Locator, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # ---------------------------------------------------------------- actions
    def click(self, locator: Locator) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        try:
            element.click()
        except ElementClickInterceptedException:
            # Something (sticky header, banner) covers the element: fall back to JS click
            self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator: Locator, text: str, clear: bool = True) -> None:
        element = self.visible(locator)
        if clear:
            element.clear()
        element.send_keys(str(text))

    def text_of(self, locator: Locator) -> str:
        return self.visible(locator).text.strip()

    # ------------------------------------------------ popups / alerts handling
    def handle_alert_if_present(self, timeout: float = 1.5, accept: bool = True) -> Optional[str]:
        """Handle a native JavaScript alert/confirm if one is showing.

        Returns the alert text when one was handled, otherwise None. Safe to call at any
        time: it never fails when no alert exists.
        """
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        except TimeoutException:
            return None
        text = alert.text
        log.info("JS alert found: %r -> %s", text, "accept" if accept else "dismiss")
        alert.accept() if accept else alert.dismiss()
        return text

    def close_banners(self) -> int:
        """Close any in-page dismissible alert banners (HTML popups). Returns how many."""
        closed = 0
        for btn in self.driver.find_elements(*self.ALERT_CLOSE_BTN):
            try:
                if btn.is_displayed():
                    btn.click()
                    closed += 1
            except Exception:  # banner may vanish on its own while we click
                pass
        if closed:
            log.info("Closed %d alert banner(s)", closed)
        return closed

    def success_message(self, timeout: Optional[int] = None) -> str:
        return self.visible(self.SUCCESS_BANNER, timeout).text.replace("×", "").strip()

    def error_message(self, timeout: Optional[int] = None) -> str:
        return self.visible(self.DANGER_BANNER, timeout).text.replace("×", "").strip()
