"""Product catalog browsing and sorting."""
import pytest


@pytest.mark.mobile
def test_catalog_loads_with_products(catalog_screen):
    assert catalog_screen.is_shown()
    assert catalog_screen.items_count() > 0


@pytest.mark.mobile
def test_sort_by_price_ascending_updates_active_option(catalog_screen, sort_modal):
    catalog_screen.open_sort_modal()
    sort_modal.sort_price_asc()

    catalog_screen.open_sort_modal()
    assert sort_modal.get_active_option_text().strip() != ""


@pytest.mark.mobile
def test_sort_by_name_ascending_updates_active_option(catalog_screen, sort_modal):
    catalog_screen.open_sort_modal()
    sort_modal.sort_name_asc()

    catalog_screen.open_sort_modal()
    assert sort_modal.get_active_option_text().strip() != ""


@pytest.mark.mobile
def test_open_first_item_shows_item_details(catalog_screen, item_details_screen):
    first_item_name = catalog_screen.get_item_name(0)
    catalog_screen.open_item_by_name(first_item_name)

    assert item_details_screen.is_shown()
