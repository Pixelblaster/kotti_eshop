from kotti.util import LinkParent, Link
from kotti_eshop.util import RouteLink
from kotti_eshop.util import RootLink
from pyramid.view import view_config
from kotti_eshop import _
from kotti_eshop import ShopRoot


admin_links = LinkParent(_("Options"), children=[
    RouteLink('kotti_eshop', title=_(u'Main'), traverse=[]),
    Link('products', title=_("Manage products")),
    Link('clients', title=_("Manage clients")),
    Link('orders', title=_("Manage orders")),
    RootLink('settings', title=_("Shop settings")),
])


@view_config(name="shop-admin-menu", permission="view",
             context=ShopRoot,
             renderer="kotti_eshop:templates/shop-admin-menu.pt")
def shop_admin_menu(context, request):
    return {'links': admin_links}
