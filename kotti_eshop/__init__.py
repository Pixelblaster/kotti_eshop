# -*- coding: utf-8 -*-

from kotti.resources import Document
from kotti.resources import default_actions
from kotti.util import LinkRenderer
from kotti.views.site_setup import CONTROL_PANEL_LINKS
from kotti.views.slots import assign_slot
from pyramid.i18n import TranslationStringFactory
from kotti_eshop.util import RouteLink


_ = TranslationStringFactory('kotti_eshop')


def kotti_configure(settings):
    s = settings
    s['kotti.populators'] += ' kotti_eshop.populate.populate'
    s['pyramid.includes'] += ' kotti_eshop'
    s['kotti.fanstatic.view_needed'] += ' kotti_eshop.fanstatic.css_and_js'
    s['kotti.templates.api'] = 'kotti_eshop.resources.TemplateAPI'

    settings = RouteLink('kotti_eshop', title=_(u'Kotti E-Shop Management'))
    CONTROL_PANEL_LINKS.append(settings)

    Document.type_info.selectable_default_views.append(
        ('shop_view', 'Shop View'))

    default_actions.children.append(LinkRenderer("assign-product-menu-entry"))


class DummyRoot(object):
    __name__ = ''
    __parent__ = None
    title = _("Root")


class ShopRoot(object):
    __name__ = '-shop'
    __parent__ = DummyRoot()
    title = _("Kotti E-Shop Administration")

    def __getitem__(self, name):
        print "getting", name


def get_shop_root(request):
    return ShopRoot()


def includeme(config):

    config.add_translation_dirs('kotti_eshop:locale')
    config.add_static_view('static-kotti_eshop', 'kotti_eshop:static')
    config.add_route("kotti_eshop", "/-shop/*traverse", factory=get_shop_root)

    config.scan(__name__)

    assign_slot('shopping_cart', 'abovecontent')

