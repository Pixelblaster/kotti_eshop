# -*- coding: utf-8 -*-

from pyramid.i18n import TranslationStringFactory
from kotti.resources import Document
from kotti.util import ViewLink
from kotti.views.slots import assign_slot
from kotti.views.site_setup import CONTROL_PANEL_LINKS

_ = TranslationStringFactory('kotti_eshop')


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_eshop.kotti_configure

        to enable the ``kotti_eshop`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['kotti.populators'] += ' kotti_eshop.populate.populate'
    settings['pyramid.includes'] += ' kotti_eshop'
    settings['kotti.fanstatic.view_needed'] += \
        ' kotti_eshop.fanstatic.css_and_js'

    settings = ViewLink('shop_admin', title=_(u'Shop Admin'))
    CONTROL_PANEL_LINKS.append(settings)

    Document.type_info.selectable_default_views.append(
        ('shop_view', 'Shop View'))


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('kotti_eshop:locale')
    config.add_static_view('static-kotti_eshop', 'kotti_eshop:static')

    config.scan(__name__)
    assign_slot('shopping_cart', 'abovecontent')
