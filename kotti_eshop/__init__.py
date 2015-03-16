# -*- coding: utf-8 -*-

#from kotti.resources import Content
from kotti.resources import default_actions
from kotti.resources import Document
from kotti.util import Link, LinkRenderer
from kotti.views.site_setup import CONTROL_PANEL_LINKS
from kotti.views.slots import assign_slot
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_eshop')


def kotti_configure(settings):
    s = settings
    s['kotti.populators'] += ' kotti_eshop.populate.populate'
    s['pyramid.includes'] += ' kotti_eshop'
    s['kotti.fanstatic.view_needed'] += ' kotti_eshop.fanstatic.css_and_js'
    s['kotti.templates.api'] = 'kotti_eshop.resources.TemplateAPI'

    settings = Link('shop_admin', title=_(u'Shop Admin'))
    CONTROL_PANEL_LINKS.append(settings)

    Document.type_info.selectable_default_views.append(
        ('shop_view', 'Shop View'))

    default_actions.children.append(LinkRenderer("assign-product-menu-entry"))


def includeme(config):

    config.add_translation_dirs('kotti_eshop:locale')
    config.add_static_view('static-kotti_eshop', 'kotti_eshop:static')

    config.scan(__name__)
    assign_slot('shopping_cart', 'abovecontent')
