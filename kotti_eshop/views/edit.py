#import colander
from kotti.views.edit.content import ContentSchema
from kotti.views.form import AddFormView
from kotti_eshop.resources import ShopProduct
from pyramid.view import view_config
from kotti_eshop import _


class ProductSchema(ContentSchema):
    """
    """


@view_config(name="add-product", permission="view",
             renderer="kotti:templates/edit/node.pt")
class ProductAddForm(AddFormView):
    schema_factory = ProductSchema
    add = ShopProduct
    item_type = _(u"Product")


@view_config(name='assign-product', permission='view',
             renderer='kotti_eshop:templates/edit/assign.pt')
def assign_product(context, request):
    return {}
