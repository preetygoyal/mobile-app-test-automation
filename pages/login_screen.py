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

    # timeout=8, not 3: these are checked right after submitting the login
    # form, and a run was observed where the inline validation error simply
    # hadn't rendered yet within 3s under CI's slower emulator, so the check
    # gave up and returned "" -- read as a real assertion failure ("app
    # didn't show the error") when it was actually "app hadn't finished
    # rendering it yet". These are always called expecting the error *to*
    # be there, so a longer wait costs nothing on a healthy run.
    def get_username_error(self) -> str:
        return self.find(self.USERNAME_ERROR).text if self.is_displayed(self.USERNAME_ERROR, timeout=8) else ""

    def get_password_error(self) -> str:
        return self.find(self.PASSWORD_ERROR).text if self.is_displayed(self.PASSWORD_ERROR, timeout=8) else ""

    def get_generic_error(self) -> str:
        return self.find(self.GENERIC_ERROR).text if self.is_displayed(self.GENERIC_ERROR, timeout=8) else ""
