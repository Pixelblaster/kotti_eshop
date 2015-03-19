from kotti.util import LinkParent, Link #, RouteLink
from pyramid.view import view_config
from kotti_eshop import _


admin_links = LinkParent(_("Options"), children=[
    Link('', _("Main")),
])
      # <li class="list-group-item">
      #   <a href="${api.url(context)}">Main</a>
      # </li>
      # <li class="list-group-item">
      #   <a href="${api.url(context)}@@add-product">Add a product</a>
      # </li>
      # <li class="list-group-item">
      #   <a href="${api.url(context)}@@products">
      #     Manage products
      #   </a>
      # </li>
      # <li class="list-group-item">
      #   <a href="${api.url(context)}@@clients">
      #     Manage clients
      #   </a>
      # </li>
      # <li class="list-group-item">
      #   <a href="${api.url(api.root,'@@settings')}">Edit shop settings</a>
      # </li>

@view_config(name="shop-admin-links", renderer="templates/shop-admin-menu.pt")
def shop_admin_menu(context, request):
    import pdb; pdb.set_trace()
    return {'links': admin_links}
