"""Home screen: the top-level category list and basic back navigation."""
import pytest


@pytest.mark.mobile
def test_home_screen_shows_top_level_categories(home_screen):
    assert home_screen.is_shown()
    assert home_screen.scroll_to_text("App") is not None
    assert home_screen.scroll_to_text("Views") is not None


@pytest.mark.mobile
def test_back_button_returns_to_home_from_category(home_screen, alert_dialog_screen):
    home_screen.open("App", "Alert Dialogs")
    assert alert_dialog_screen.is_shown()

    home_screen.driver.back()
    assert home_screen.is_shown()
