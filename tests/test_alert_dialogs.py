"""App/Alert Dialogs: opening and dismissing a simple OK/Cancel dialog."""
import pytest


@pytest.mark.mobile
def test_two_buttons_dialog_shows_and_ok_dismisses(home_screen, alert_dialog_screen):
    home_screen.open("App", "Alert Dialogs")
    assert alert_dialog_screen.is_shown()

    alert_dialog_screen.open_two_buttons_dialog()
    assert alert_dialog_screen.is_dialog_shown()

    alert_dialog_screen.tap_ok()
    assert not alert_dialog_screen.is_dialog_shown()


@pytest.mark.mobile
def test_two_buttons_dialog_cancel_dismisses(home_screen, alert_dialog_screen):
    home_screen.open("App", "Alert Dialogs")
    assert alert_dialog_screen.is_shown()

    alert_dialog_screen.open_two_buttons_dialog()
    assert alert_dialog_screen.is_dialog_shown()

    alert_dialog_screen.tap_cancel()
    assert not alert_dialog_screen.is_dialog_shown()
