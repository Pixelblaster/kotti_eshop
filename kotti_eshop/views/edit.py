from pyramid.view import view_config

@view_config(name='edit-as-product', permission='view',
             renderer='kotti_eshop:templates/edit/product.pt')
def edit_as_product(context, request):
    return {}
