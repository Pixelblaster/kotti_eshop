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
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults
import colander


def unique_pin(node, pin):
    """ Product Identification Number must be unique.
    """
    products = DBSession.query(BackendProduct.id).filter_by(pin=pin).count()

    if products:
        msg = _(u'This Unique Product Identification Number $pin is already '
                u'in database.', mapping={'pin': pin})
        raise colander.Invalid(node, msg)


@colander.deferred
def deferred_edit_product_validator(node, kw):

    def unique_pin(node, pin):
        """ Check if the given pin already exists for Edit view
        """
        request = kw.get('request')
        product_id = request.GET.get('product_id')

        product = DBSession.query(BackendProduct).filter_by(pin=pin).first()

        if product is None:
            return

        context = None
        if product_id:
            context = DBSession.query(BackendProduct).get(int(product_id))

        if product != context:
            msg = _(u'This Unique Product Identification Number $pin is '
                    u'already in database.', mapping={'pin': pin})
            raise colander.Invalid(node, msg)

    return unique_pin


class BackendProductSchema(colander.MappingSchema):
    """ Schema for edit product
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
    pin = colander.SchemaNode(
        colander.String(),
        title=_(u'Product Identification Number'),
        validator=deferred_edit_product_validator,
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
    first_heading = (u"Edit product details")

    @reify
    def success_url(self):
        root = get_root()
        return self.request.resource_url(root) + \
            '@@shop_admin?action=products'

    def before(self, form):
        get = self.request.GET
        product_id = get.get('product_id', None)
        if product_id is not None:
            product = DBSession.query(BackendProduct).filter(
                BackendProduct.id == product_id).first()
            if product:
                form.appstruct = get_appstruct(self.context, self.schema)
                form.appstruct.update({
                    'pin': product.pin,
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
                BackendProduct.id == int(product_id)).first()
            if product:
                product.pin = appstruct['pin']
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


@view_config(name='shop_admin', permission="manage",
                renderer='kotti_eshop:templates/shop-admin-view.pt')
class AdminViews(BaseFormView):
    """ Shop administration panel
    """

    schema_factory = SchemaNode

    def delete_backend_product_success(self, appstruct):
        product_id = self.request.params.get('backend_product_id', None)
        if product_id is not None:
            product = DBSession.query(BackendProduct).filter(
                BackendProduct.id == product_id).first()
            if product:
                DBSession.delete(product)
                root = get_root()
                return HTTPFound(location=self.request.resource_url(root) +
                                    '@@shop_admin?action=products')

    def delete_product_assignment_success(self):
        product_id = self.request.params.get('backend_product_id', None)
        content_item_id = self.request.params.get('content_item_id', None)
        if product_id is not None and content_item_id is not None:
            product = DBSession.query(BackendProduct).filter(
                BackendProduct.id == product_id).first()
            if product:
                for content in product.assigned_content:
                    if content.id == int(content_item_id):
                        product.assigned_content.remove(content)

                root = get_root()
                return HTTPFound(location=self.request.resource_url(root) +
                                    '@@shop_admin?action=products')


@view_defaults(permission="view")
class ShoppingCartViews(BaseView):

    @view_config(name='cart_operations',
                 renderer='kotti:templates/edit/node.pt')
    def cart_operations(self):
        """ Operation with a shopping cart
        """
        # ADD to cart
        if 'add_to_cart' in self.request.params:
            product_id = self.request.params.get('backend_product_id', None)
            quantity = int(self.request.params.get('quantity', 0))
            if product_id is not None and quantity > 0:
                pass
                # [TODO]
                # check session for uuid
                # create or get shopping cart with this uuid
                # add product * quantity to cart
                # redirect to cart view?
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root))


@view_config(
    name="assign-product-menu-entry", permission="edit",
    renderer="kotti_eshop:templates/edit/assign-product-menu-entry.pt")
def assign_product_menu_entry(context, request):
    return {}
