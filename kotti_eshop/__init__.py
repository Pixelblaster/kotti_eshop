# -*- coding: utf-8 -*-

from kotti.resources import File
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_eshop')


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_eshop.kotti_configure

        to enable the ``kotti_eshop`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_eshop'
    settings['kotti.available_types'] += (
        ' kotti_eshop.resources.Shop' +
        ' kotti_eshop.resources.ShopProduct' +
        ' kotti_eshop.resources.ProductImage' +
        ' kotti_eshop.resources.CustomContent')
    settings['kotti.fanstatic.view_needed'] += \
        ' kotti_eshop.fanstatic.css_and_js'
    File.type_info.addable_to.append('CustomContent')


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('kotti_eshop:locale')
    config.add_static_view('static-kotti_eshop', 'kotti_eshop:static')

    config.scan(__name__)
