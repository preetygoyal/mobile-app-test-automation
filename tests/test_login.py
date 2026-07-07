"""
Login scenarios against the demo app's real auth behaviour: valid login,
invalid credentials, a locked-out account, missing-field validation, and
logout. Credentials and expected error copy come straight from the app's
own source (see tests/test_data.py), not guessed.
"""
import pytest

from tests.test_data import (
    ERROR_LOCKED_OUT,
    ERROR_NO_MATCH,
    ERROR_PASSWORD_REQUIRED,
    ERROR_USERNAME_REQUIRED,
    LOCKED_OUT_USER,
    NO_MATCH_USER,
    STANDARD_USER,
)


@pytest.mark.mobile
def test_login_with_valid_credentials(menu_screen, login_screen):
    menu_screen.open_menu()
    menu_screen.open_login()
    assert login_screen.is_shown()

    login_screen.login(**STANDARD_USER)

    menu_screen.open_menu()
    assert menu_screen.is_logged_in()


@pytest.mark.mobile
def test_login_with_no_matching_credentials_shows_error(menu_screen, login_screen):
    menu_screen.open_menu()
    menu_screen.open_login()

    login_screen.login(**NO_MATCH_USER)

    assert login_screen.get_generic_error() == ERROR_NO_MATCH


@pytest.mark.mobile
def test_login_with_locked_out_account_shows_error(menu_screen, login_screen):
    menu_screen.open_menu()
    menu_screen.open_login()

    login_screen.login(**LOCKED_OUT_USER)

    assert login_screen.get_generic_error() == ERROR_LOCKED_OUT


@pytest.mark.mobile
def test_login_missing_username_shows_error(menu_screen, login_screen):
    menu_screen.open_menu()
    menu_screen.open_login()

    login_screen.login(username="", password=STANDARD_USER["password"])

    assert login_screen.get_username_error() == ERROR_USERNAME_REQUIRED


@pytest.mark.mobile
def test_login_missing_password_shows_error(menu_screen, login_screen):
    menu_screen.open_menu()
    menu_screen.open_login()

    login_screen.login(username=STANDARD_USER["username"], password="")

    assert login_screen.get_password_error() == ERROR_PASSWORD_REQUIRED


@pytest.mark.mobile
def test_logout_returns_to_logged_out_state(menu_screen, login_screen):
    menu_screen.open_menu()
    menu_screen.open_login()
    login_screen.login(**STANDARD_USER)

    menu_screen.open_menu()
    assert menu_screen.is_logged_in()
    menu_screen.logout()

    menu_screen.open_menu()
    assert not menu_screen.is_logged_in()
