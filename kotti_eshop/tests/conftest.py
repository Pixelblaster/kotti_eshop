# -*- coding: utf-8 -*-

"""
Created on 2015-02-18
:author: GhitaB (ghita_bizau@yahoo.com)
"""

pytest_plugins = "kotti"

from pytest import fixture


@fixture(scope='session')
def custom_settings():
    import kotti_eshop.resources
    kotti_eshop.resources  # make pyflakes happy
    return {
        'kotti.configurators': 'kotti_tinymce.kotti_configure '
                               'kotti_eshop.kotti_configure'}
