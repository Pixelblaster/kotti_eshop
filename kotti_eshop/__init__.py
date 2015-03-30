# -*- coding: utf-8 -*-

from kotti.resources import Document
from kotti.resources import default_actions
from kotti.security import SITE_ACL
from kotti.util import LinkRenderer
from kotti.views.site_setup import CONTROL_PANEL_LINKS
from kotti.views.slots import assign_slot
from pyramid.i18n import TranslationStringFactory
from kotti_eshop.util import RouteLink
from anykeystore import create_store_from_settings
from kotti.events import objectevent_listeners
from kotti_accounts import kotti_configure_events
from kotti_velruse.events import AfterKottiVelruseLoggedIn
from kotti_velruse.events import AfterLoggedInObject

_ = TranslationStringFactory('kotti_eshop')


def kotti_configure(settings):
    s = settings
    s['kotti.populators'] += ' kotti_eshop.populate.populate'
    s['pyramid.includes'] += ' kotti_eshop velruse.app'
    s['kotti.fanstatic.view_needed'] += ' kotti_eshop.fanstatic.css_and_js'
    s['kotti.templates.api'] = 'kotti_eshop.resources.TemplateAPI'

    shop = RouteLink('kotti_eshop', title=_(u'Kotti E-Shop Management'),
                     traverse=[])
    CONTROL_PANEL_LINKS.append(shop)

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
    __acl__ = SITE_ACL

    def __getitem__(self, name):
        print "getting", name


def configure_velruse(config):
    """ Configure velruse to avoid a conflict error about the session setup
    """

    # setup velruse backing storage
    settings = config.registry.settings
    storage_string = settings.get('store')
    settings['store.store'] = storage_string
    store = create_store_from_settings(settings, prefix='store.')
    config.register_velruse_store(store)

    # configure velruse integration through kotti_accounts/kotti_velruse
    kotti_configure_events(settings)
    config.include('velruse.providers.facebook')
    config.add_facebook_login_from_settings(prefix='velruse.facebook.')

    # FOR EACH LOGGED IN: get_extra_info
    #import pdb; pdb.set_trace( )
    # objectevent_listeners[(
    #     AfterKottiVelruseLoggedIn, AfterLoggedInObject)].append(
    #     get_extra_info)


def includeme(config):

    config.add_translation_dirs('kotti_eshop:locale')
    config.add_static_view('static-kotti_eshop', 'kotti_eshop:static')
    config.add_route("kotti_eshop", "/-shop/*traverse",
                     factory=lambda request: ShopRoot())

    config.scan(__name__)

    assign_slot('shopping_cart', 'abovecontent')
