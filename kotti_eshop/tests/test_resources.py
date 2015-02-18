# -*- coding: utf-8 -*-

"""
Created on 2015-02-18
:author: GhitaB (ghita_bizau@yahoo.com)
"""

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
