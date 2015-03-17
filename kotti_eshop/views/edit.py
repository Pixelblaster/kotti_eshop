from deform.widget import MoneyInputWidget
from deform.widget import RichTextWidget
from deform.widget import TextAreaWidget
from kotti_eshop.views import BaseView
from kotti.resources import DBSession
from kotti.resources import get_root
from kotti.views.form import BaseFormView
from kotti.views.form import EditFormView
from kotti.views.form import get_appstruct
from kotti_eshop import _
from kotti_eshop.fanstatic import selectize
from kotti_eshop.resources import BackendProduct
from kotti_eshop.views.widget import SelectizeWidget
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults
import colander


def unique_product_id(node, value):
    """ Product ID must be unique.
    """
    products = DBSession.query(BackendProduct.id).filter_by(
        product_id=value).count()

    if products:
        msg = _(u'Product with ID $product_id is already in database.',
                mapping={'product_id': value})
        raise colander.Invalid(node, msg)


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
    product_id = colander.SchemaNode(
        colander.String(),
        title=_(u'Unique product ID'),
        validator=unique_product_id,
        )


@view_config(name="add-product", permission="view",
             renderer="kotti:templates/edit/node.pt")
class BackendProductAddForm(BaseFormView):
    """ A form view to instantiate a new BackendProduct
    """
    schema_factory = BackendProductSchema
    success_message = _(u"Product added")

    def save_success(self, appstruct):
        appstruct.pop('csrf_token', None)
        product = BackendProduct(**appstruct)
        DBSession.add(product)


@view_config(name="edit-product", permission="view",
             renderer="kotti:templates/edit/node.pt")
class BackendProductEditForm(EditFormView):
    """ A form view to edit a BackendProduct
        Example: www.mykottisite.com/@@edit_product?product_id=3
    """
    schema_factory = BackendProductSchema
    success_message = _(u"Product details saved.")

    def before(self, form):
        get = self.request.GET
        product_id = get.get('product_id', None)
        if product_id is not None:
            product = DBSession.query(BackendProduct).filter(
                BackendProduct.id == product_id).first()
            if product:
                form.appstruct = get_appstruct(self.context, self.schema)
                form.appstruct.update({
                    'product_id': product.product_id,
                    'title': product.title,
                    'description': product.description,
                    'text': product.description,
                    'price': float(product.price),
                })

    def edit(self, **appstruct):
        get = self.request.GET
        product_id = get.get('product_id', None)
        if product_id is not None:
            product = DBSession.query(BackendProduct).filter(
                BackendProduct.id == product_id).first()
            if product:
                product.product_id = appstruct['product_id']
                product.title = appstruct['title']
                product.description = appstruct['description']
                product.text = appstruct['text']
                product.price = appstruct['price']
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root) +
                         '@@shop_admin?action=products')


class ProductType(colander.Integer):

    def deserialize(self, node, cstruct):
        return DBSession.query(BackendProduct).get(int(cstruct))

    def serialize(self, node, cstruct):
        if cstruct is colander.null:
            return

        return str(cstruct.id)


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
             # renderer='kotti_eshop:templates/edit/assign.pt')
             renderer='kotti:templates/edit/node.pt')
class AssignBackendProductForm(BaseFormView):
    """ A form view to assign a ShopProduct to the context Content derivate
    """
    schema_factory = AssignBackendProductSchema

    def appstruct(self):
        return {'products': self.context.backend_products}

    def save_success(self, appstruct):
        self.context.backend_products = list(appstruct['products'])

    def before(self, form):
        selectize.need()
        return super(AssignBackendProductForm, self).before(form)


@view_defaults(permission="manage")
class AdminViews(BaseView):

    @view_config(name='shop_admin',
                 renderer='kotti_eshop:templates/shop-admin-view.pt')
    def shop_admin_view(self):
        """ Shop administration panel
        """
        if 'delete_backend_product' in self.request.params:
            product_id = self.request.params.get('backend_product_id', None)
            if product_id is not None:
                product = DBSession.query(BackendProduct).filter(
                    BackendProduct.id == product_id).first()
                if product:
                    DBSession.delete(product)
                    root = get_root()
                    return HTTPFound(location=self.request.resource_url(root) +
                                     '@@shop_admin?action=products')
        return {}


@view_config(
    name="assign-product-menu-entry", permission="edit",
    renderer="kotti_eshop:templates/edit/assign-product-menu-entry.pt")
def assign_product_menu_entry(context, request):
    return {}
