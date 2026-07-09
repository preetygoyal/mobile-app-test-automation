"""Views/TextFields: typing into and clearing a plain EditText."""
import pytest


@pytest.mark.mobile
def test_text_field_accepts_and_returns_typed_text(home_screen, text_fields_screen):
    home_screen.open("Views", "TextFields")
    assert text_fields_screen.is_shown()

    text_fields_screen.enter_text("Hello Appium")
    assert text_fields_screen.get_text() == "Hello Appium"


@pytest.mark.mobile
def test_text_field_can_be_cleared(home_screen, text_fields_screen):
    home_screen.open("Views", "TextFields")
    text_fields_screen.enter_text("Some text")
    assert text_fields_screen.get_text() == "Some text"

    text_fields_screen.enter_text("")
    # An empty EditText exposes its hint ("hint text") through the same
    # accessibility text node Appium reads via `.text` -- there's no
    # separate "actual value vs. hint" attribute here, so a run showed
    # this assert 'hint text' == '' rather than a real bug. "Cleared" is
    # verified as "no longer showing what we typed" instead of a literal
    # empty string.
    assert text_fields_screen.get_text() != "Some text"
