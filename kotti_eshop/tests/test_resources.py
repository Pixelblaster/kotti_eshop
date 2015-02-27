# -*- coding: utf-8 -*-
from pytest import raises


def test_model(root, db_session):
    from kotti_eshop.resources import CustomContent

    cc = CustomContent()
    assert cc.custom_attribute is None

    cc = CustomContent(custom_attribute=u'Foo')
    assert cc.custom_attribute == u'Foo'

    root['cc'] = cc = CustomContent()
    assert cc.name == 'cc'

    with raises(TypeError):
        cc = CustomContent(doesnotexist=u'Foo')


def test_shop_model(root, db_session):
    from kotti_eshop.resources import Shop

    shop = Shop()
    assert shop.name is None

    shop = Shop(title=u'Shop')
    assert shop.title == u'Shop'

    root['shopname'] = shop = Shop()
    assert shop.name == 'shopname'

    with raises(TypeError):
        shop = Shop(doesnotexist=u'Foo')
