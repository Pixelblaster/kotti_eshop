# -*- coding: utf-8 -*-
from pytest import fixture


@fixture
def dummy_content(root):

    from kotti_eshop.resources import CustomContent

    root['cc'] = cc = CustomContent(
        title=u'My content',
        description=u'My very custom content is custom',
        custom_attribute='Lorem ipsum'
    )

    return cc


def test_view(dummy_content, dummy_request):

    from kotti_eshop.views.view import CustomContentViews

    views = CustomContentViews(dummy_content, dummy_request)

    default = views.default_view()
    assert 'foo' in default

    alternative = views.alternative_view()
    assert alternative['foo'] == u'bar'


@fixture
def dummy_shop(root):
    """ Returns a shop for tests """
    from kotti_eshop.resources import Shop

    root['shop'] = shop = Shop(
        title=u'My Shop',
        description=u'My very custom content is custom'
    )

    return shop


def test_shop_views(dummy_shop, dummy_request):

    from kotti_eshop.views.view import ShopViews

    views = ShopViews(dummy_shop, dummy_request)

    # test admin view
    shop_admin_view = views.shop_admin_view()
    assert 'custom_page_title' in shop_admin_view
    assert 'products' in shop_admin_view
    assert 'today' in shop_admin_view

    # test shopping cart view
    from kotti_eshop.views.view import shopping_cart
    shopping_cart_view = shopping_cart(dummy_request)
    assert 'logged_in_user' in shopping_cart_view
