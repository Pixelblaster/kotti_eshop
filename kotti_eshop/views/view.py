# -*- coding: utf-8 -*-
from pyramid.view import view_config
from kotti_eshop.resources import currency
from kotti_eshop.resources import get_all_clients
from kotti_eshop.resources import get_all_products
from kotti_eshop.resources import products_per_page


@view_config(name='shopping_cart', permission='view',
             renderer='kotti_eshop:templates/shopping-cart.pt')
def shopping_cart(request):
    """ Shopping cart view
    """
    if request.user:
        logged_in_user = request.user.name
    else:
        logged_in_user = ''
    return {'logged_in_user': logged_in_user}


@view_config(name='shop_admin', permission='view',
             renderer='kotti_eshop:templates/shop-admin-view.pt')
def shop_admin_view(self):
    """ Shop administration panel
    """
    return {'shop_products_per_page': products_per_page(),
            'shop_currency': currency(),
            'shop_clients': get_all_clients(),
            'products': get_all_products()}


@view_config(name='shop_view', permission='view',
             renderer='kotti_eshop:templates/shop-view.pt')
def shop_view(self):
    """ Shop view
    """
    custom_page_title = "Administration Panel"
    products = get_all_products()
    return {'shop_products_per_page': products_per_page(),
            'shop_currency': currency(),
            'shop_clients': get_all_clients(),
            'products': products,
            'custom_page_title': custom_page_title}
