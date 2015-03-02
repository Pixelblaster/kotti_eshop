# -*- coding: utf-8 -*-
from pytest import raises


def test_shop_resources(root, db_session):
    # shop
    from kotti_eshop.resources import Shop

    shop = Shop()
    assert shop.name is None

    shop = Shop(title=u'Shop')
    assert shop.title == u'Shop'

    root['shopname'] = shop = Shop()
    assert shop.name == 'shopname'

    assert shop.get_all_clients().count() == 0

    with raises(TypeError):
        shop = Shop(doesnotexist=u'Foo')

    # product
    from kotti_eshop.resources import ShopProduct
    product = ShopProduct()
    assert product.name is None

    root['shopname']['productname'] = product = ShopProduct()
    assert product.name == 'productname'

    # product image
    from kotti_eshop.resources import ProductImage
    image = ProductImage()
    assert image.name is None

    root['shopname']['productname']['imagename'] = image = ProductImage()
    assert image.name == 'imagename'
