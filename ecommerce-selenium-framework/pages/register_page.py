from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegisterPage(BasePage):
    FIRST_NAME = (By.ID, "input-firstname")
    LAST_NAME = (By.ID, "input-lastname")
    EMAIL = (By.ID, "input-email")
    TELEPHONE = (By.ID, "input-telephone")
    PASSWORD = (By.ID, "input-password")
    CONFIRM = (By.ID, "input-confirm")
    PRIVACY_POLICY = (By.NAME, "agree")
    CONTINUE_BTN = (By.CSS_SELECTOR, "input[value='Continue']")
    HEADING = (By.CSS_SELECTOR, "#content h1")

    def load(self) -> "RegisterPage":
        self.open_route("account/register")
        return self

    def register(self, first_name: str, last_name: str, email: str,
                 telephone: str, password: str) -> str:
        """Fill the form, submit, and return the confirmation heading text."""
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.EMAIL, email)
        self.type(self.TELEPHONE, telephone)
        self.type(self.PASSWORD, password)
        self.type(self.CONFIRM, password)
        self.click(self.PRIVACY_POLICY)
        self.click(self.CONTINUE_BTN)
        return self.text_of(self.HEADING)
