from kotti.resources import DBSession
from kotti_eshop.resources import BackendProduct
from pyramid.exceptions import PredicateMismatch
from pyramid.view import view_config


@view_config(name='shopping_cart', permission='view',
             renderer='kotti_eshop:templates/shopping-cart.pt')
def shopping_cart(context, request):
    """ Shopping cart view
    """

    has_backend_products = DBSession.query(BackendProduct.id).count()

    if not has_backend_products:
        raise PredicateMismatch()

    backend_product = None
    backend_product_id = None
    backend_product_title = ""
    backend_product_description = ""
    backend_product_price = None
    if context.backend_products:
        backend_product = context.backend_products[0]
        backend_product_id = backend_product.id
        backend_product_title = backend_product.title
        backend_product_description = backend_product.description
        backend_product_price = float(backend_product.price)
    if request.user:
        logged_in_user = request.user.name
    else:
        logged_in_user = ''

    return {'has_backend_products': has_backend_products,
            'backend_product_id': backend_product_id,
            'backend_product_title': backend_product_title,
            'backend_product_description': backend_product_description,
            'backend_product_price': backend_product_price,
            'logged_in_user': logged_in_user,
            'backend_product': backend_product}


@view_config(name='shop_view', permission='view',
             renderer='kotti_eshop:templates/shop-view.pt')
def shop_view(self):
    """ Shop view
    """
    return {}
