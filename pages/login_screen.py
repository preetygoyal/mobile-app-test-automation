from .base_screen import BaseScreen


class LoginScreen(BaseScreen):
    USERNAME_FIELD = "Username input field"
    PASSWORD_FIELD = "Password input field"
    LOGIN_BUTTON = "Login button"
    USERNAME_ERROR = "Username-error-message"
    PASSWORD_ERROR = "Password-error-message"
    GENERIC_ERROR = "generic-error-message"
    LOGIN_SCREEN = "login screen"

    def is_shown(self) -> bool:
        return self.is_displayed(self.LOGIN_SCREEN, timeout=10)

    def login(self, username: str = "", password: str = ""):
        if username:
            self.find(self.USERNAME_FIELD).send_keys(username)
        if password:
            self.find(self.PASSWORD_FIELD).send_keys(password)
        self.find(self.LOGIN_BUTTON).click()

    def get_username_error(self) -> str:
        return self.find(self.USERNAME_ERROR).text if self.is_displayed(self.USERNAME_ERROR, timeout=3) else ""

    def get_password_error(self) -> str:
        return self.find(self.PASSWORD_ERROR).text if self.is_displayed(self.PASSWORD_ERROR, timeout=3) else ""

    def get_generic_error(self) -> str:
        return self.find(self.GENERIC_ERROR).text if self.is_displayed(self.GENERIC_ERROR, timeout=3) else ""
