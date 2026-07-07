"""Add-to-cart, quantity, and cart management flows."""
import pytest


@pytest.mark.mobile
def test_empty_cart_shows_go_shopping(cart_screen):
    cart_screen.open_cart()
    assert cart_screen.is_shown()
    assert cart_screen.items_count() == 0


@pytest.mark.mobile
def test_add_single_item_to_cart(catalog_screen, item_details_screen, cart_screen):
    first_item_name = catalog_screen.get_item_name(0)
    catalog_screen.open_item_by_name(first_item_name)
    assert item_details_screen.is_shown()

    item_details_screen.add_to_cart()

    cart_screen.open_cart()
    assert cart_screen.items_count() == 1


@pytest.mark.mobile
def test_increase_quantity_before_adding_to_cart(catalog_screen, item_details_screen):
    first_item_name = catalog_screen.get_item_name(0)
    catalog_screen.open_item_by_name(first_item_name)

    starting_amount = item_details_screen.get_quantity()
    item_details_screen.increase_quantity()

    assert item_details_screen.get_quantity() == starting_amount + 1


@pytest.mark.mobile
def test_proceed_to_checkout_visible_once_cart_has_an_item(catalog_screen, item_details_screen, cart_screen):
    first_item_name = catalog_screen.get_item_name(0)
    catalog_screen.open_item_by_name(first_item_name)
    item_details_screen.add_to_cart()

    cart_screen.open_cart()
    assert cart_screen.proceed_to_checkout_visible()


@pytest.mark.mobile
def test_remove_item_empties_the_cart(catalog_screen, item_details_screen, cart_screen):
    first_item_name = catalog_screen.get_item_name(0)
    catalog_screen.open_item_by_name(first_item_name)
    item_details_screen.add_to_cart()

    cart_screen.open_cart()
    assert cart_screen.items_count() == 1

    cart_screen.remove_item(first_item_name)
    assert cart_screen.items_count() == 0
