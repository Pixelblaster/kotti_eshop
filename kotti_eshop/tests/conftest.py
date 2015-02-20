# -*- coding: utf-8 -*-
from pytest import fixture

pytest_plugins = "kotti"


@fixture(scope='session')
def custom_settings():
    import kotti_eshop.resources
    kotti_eshop.resources  # make pyflakes happy
    return {
        'kotti.configurators': 'kotti_tinymce.kotti_configure '
                               'kotti_eshop.kotti_configure'}
