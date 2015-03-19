# -*- coding: utf-8 -*-
from pytest import raises
from kotti.testing import DummyRequest
from mock import patch


class TestKottiEshopTemplateAPI:
    """ Test kotti_eshop TemplateAPI
    """
    def make(self, context=None, request=None, id=1, **kwargs):
        from kotti.resources import get_root
        from kotti_eshop.resources import TemplateAPI

        if context is None:
            context = get_root()
        if request is None:
            request = DummyRequest()
        return TemplateAPI(context, request, **kwargs)

    def test_shop_currency(self, db_session):
        """ Test shop_currency setting
        """
        with patch('kotti.views.util.get_settings',
                   return_value={'kotti.shop_currency': None}):
            api = self.make()
            assert api.shop_currency() is None

    def test_get_all_backend_products(self, db_session):
        """ Test api.get_all_backend_products()
        """
        with patch('kotti.views.util.get_settings',
                   return_value={'kotti.get_all_backend_products': []}):
            api = self.make()
            assert api.get_all_backend_products() is not None

    def test_get_backend_product(self, db_session):
        """ Test api.get_all_backend_products()
        """
        with patch('kotti.views.util.get_settings',
                   return_value={'kotti.get_backend_product': []}):
            api = self.make()
            assert api.get_backend_product(product_id=100000) is not None


def test_backendproduct(root, db_session):
    """ Test BackendProduct in resources
    """
    from kotti_eshop.resources import BackendProduct
    assert BackendProduct is not None


def test_shop_resources(root, db_session):
    # shop
    # from kotti_eshop.resources import Shop

    # shop = Shop()
    # assert shop.name is None

    # shop = Shop(title=u'Shop')
    # assert shop.title == u'Shop'

    # root['shopname'] = shop = Shop()
    # assert shop.name == 'shopname'

    # assert shop.get_all_clients().count() == 0

    # with raises(TypeError):
    #     shop = Shop(doesnotexist=u'Foo')

    # # product
    # from kotti_eshop.resources import ShopProduct
    # product = ShopProduct()
    # assert product.name is None

    # root['shopname']['productname'] = product = ShopProduct()
    # assert product.name == 'productname'

    # # product image
    # from kotti_eshop.resources import ProductImage
    # image = ProductImage()
    # assert image.name is None

    # root['shopname']['productname']['imagename'] = image = ProductImage()
    # assert image.name == 'imagename'
    pass
