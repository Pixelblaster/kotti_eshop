from deform.widget import MoneyInputWidget
from deform.widget import RichTextWidget
from deform.widget import TextAreaWidget
from kotti.resources import DBSession
from kotti.views.form import BaseFormView
from kotti_eshop import _
from kotti_eshop.fanstatic import selectize
from kotti_eshop.resources import BackendProduct
from kotti_eshop.views.widget import SelectizeWidget
from pyramid.view import view_config
import colander


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
    text = colander.SchemaNode(
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
        appstruct.pop('csrf_token', None)
        product = BackendProduct(**appstruct)
        DBSession.add(product)


class ProductType(colander.Integer):
    def deserialize(self, node, cstruct):
        return DBSession.query(BackendProduct).get(int(cstruct))


class Products(colander.SequenceSchema):
    product_id = colander.SchemaNode(
        ProductType(),
    )


@colander.deferred
def deferred_products_widget(node, kw):
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
             #renderer='kotti_eshop:templates/edit/assign.pt')
             renderer='kotti:templates/edit/node.pt')
class AssignBackendProductForm(BaseFormView):
    """ A form view to assign a ShopProduct to the context Content derivate
    """
    schema_factory = AssignBackendProductSchema

    def appstruct(self):
        return {'products': [x.id for x in self.context.backend_products]}

    def save_success(self, appstruct):
        self.context.backend_products = list(appstruct['products'])

    def before(self, form):
        selectize.need()
        return super(AssignBackendProductForm, self).before(form)
