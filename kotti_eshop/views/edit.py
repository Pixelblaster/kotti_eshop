from deform.widget import MoneyInputWidget
from deform.widget import RichTextWidget
from deform.widget import TextAreaWidget
from kotti.resources import DBSession
from kotti.views.form import BaseFormView
from kotti_eshop import _
from kotti_eshop.resources import ShopProduct
from pyramid.view import view_config
import colander

#import colander
#from kotti.views.edit.content import ContentSchema


class ProductSchema(colander.MappingSchema):
    """
    """
    title = colander.SchemaNode(
        colander.String(),
        title=_(u'Title'),
        )
    description = colander.SchemaNode(
        colander.String(),
        title=_('Description'),
        widget=TextAreaWidget(cols=40, rows=5),
        missing=u"",
        )
    body = colander.SchemaNode(
        colander.String(),
        title=_(u'Body'),
        widget=RichTextWidget(
            # theme='advanced', width=790, height=500
        ),
        missing=u"",
        )
    price = colander.SchemaNode(
        colander.Decimal(),
        title=_(u'Base Price'),
        widget=MoneyInputWidget(),
    )


@view_config(name="add-product", permission="view",
             renderer="kotti:templates/edit/node.pt")
class ProductAddForm(BaseFormView):
    """ A form view to instantiate a new ShopProduct
    """
    schema_factory = ProductSchema
    success_message = _(u"Product added")

    def save_success(self, appstruct):
        product = ShopProduct()
        DBSession.add(product)


class AssignProductSchema(colander.MappingSchema):
    """
    """

    product = collander.


@view_config(name='assign-product', permission='view',
             renderer='kotti_eshop:templates/edit/assign.pt')
class AssignProductForm(BaseFormView):
    """ A form view to assign a ShopProduct to the context Content derivate
    """
    schema_factory = AssignProductSchema

    def save_success(self, appstruct):
        pass


def includeme(config):
    from kotti.resources import Content
    from kotti.resources import Link

    Content.type_info.edit_links.append(Link("assign-product",
                                             _("Assign a product")))
