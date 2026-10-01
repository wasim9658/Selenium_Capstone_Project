from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL = (By.ID, "input-email")
    PASSWORD = (By.ID, "input-password")
    LOGIN_BTN = (By.CSS_SELECTOR, "input[value='Login']")
    LOGOUT_LINK = (By.CSS_SELECTOR, "#column-right a[href*='account/logout']")
    ACCOUNT_HEADING = (By.XPATH, "//div[@id='content']//h2[normalize-space()='My Account']")

    def load(self) -> "LoginPage":
        self.open_route("account/login")
        return self

    def login(self, email: str, password: str) -> None:
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def is_logged_in(self, timeout: int = 5) -> bool:
        return self.is_present(self.ACCOUNT_HEADING, timeout)

    def logout(self) -> None:
        self.open_route("account/logout")
