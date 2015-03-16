# -*- coding: utf-8 -*-

from kotti.resources import Content
from kotti.resources import Document
from kotti.util import Link
from kotti.views.site_setup import CONTROL_PANEL_LINKS
from kotti.views.slots import assign_slot
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_eshop')


def kotti_configure(settings):

    settings['kotti.populators'] += ' kotti_eshop.populate.populate'
    settings['pyramid.includes'] += ' kotti_eshop'
    settings['kotti.fanstatic.view_needed'] += \
        ' kotti_eshop.fanstatic.css_and_js'

    settings = Link('shop_admin', title=_(u'Shop Admin'))
    CONTROL_PANEL_LINKS.append(settings)

    Document.type_info.selectable_default_views.append(
        ('shop_view', 'Shop View'))

    Content.type_info.edit_links.append(Link("assign-product",
                                             _("Assign a product")))


def includeme(config):

    config.add_translation_dirs('kotti_eshop:locale')
    config.add_static_view('static-kotti_eshop', 'kotti_eshop:static')

    config.scan(__name__)
    assign_slot('shopping_cart', 'abovecontent')
