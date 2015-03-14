from deform.widget import MoneyInputWidget
from deform.widget import RichTextWidget
from deform.widget import TextAreaWidget
from kotti.resources import DBSession
from kotti.views.form import BaseFormView
from kotti_eshop import _
from kotti_eshop.resources import BackendProduct
from kotti_eshop.views.widget import SelectizeWidget
from pyramid.view import view_config
import colander

#import colander
#from kotti.views.edit.content import ContentSchema


class BackendProductSchema(colander.MappingSchema):
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
        title=_(u'Product details'),
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
class BackendProductAddForm(BaseFormView):
    """ A form view to instantiate a new ShopProduct
    """
    schema_factory = BackendProductSchema
    success_message = _(u"Product added")

    def save_success(self, appstruct):
        product = BackendProduct()
        DBSession.add(product)


class Products(colander.SequenceSchema):
    product_id = colander.SchemaNode(
        colander.Integer(),
    )


def deferred_products_widget(node, **kw):
    values = DBSession.query(BackendProduct.id, BackendProduct.title).all()
    return SelectizeWidget(values=values)


class AssignBackendProductSchema(colander.MappingSchema):
    """
    """

    products = Products(
        widget=deferred_products_widget,
        title=_(u'Select products')
    )


@view_config(name='assign-product', permission='view',
             renderer='kotti_eshop:templates/edit/assign.pt')
class AssignBackendProductForm(BaseFormView):
    """ A form view to assign a ShopProduct to the context Content derivate
    """
    schema_factory = AssignBackendProductSchema

    def save_success(self, appstruct):
        pass


def includeme(config):
