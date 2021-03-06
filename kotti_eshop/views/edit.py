from datetime import datetime
from deform.widget import MoneyInputWidget
from deform.widget import RichTextWidget
from deform.widget import TextAreaWidget
from kotti.resources import DBSession
from kotti.resources import get_root
from kotti.views.form import BaseFormView
from kotti.views.form import EditFormView
from kotti.views.form import get_appstruct
from kotti_eshop import ShopRoot
from kotti_eshop import _
from kotti_eshop.fanstatic import selectize
from kotti_eshop.resources import BackendProduct
from kotti_eshop.resources import OrderStatus
from kotti_eshop.resources import ShoppingCart
from kotti_eshop.resources import ShopClient
from kotti_eshop.resources import ShopOrder
from kotti_eshop.resources import ShippingAddress
from kotti_eshop.views import BaseView
from kotti_eshop.views.widget import SelectizeWidget
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults
import colander
import deform
import uuid


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


class ShopClientSchema(colander.MappingSchema):
    """ Schema for Shop Client
    """
    email = colander.SchemaNode(
        colander.String(),
        title=_(u'Email'),
        description=_(u'To receive notifications about your order.'),
    )


@view_config(name="add-product", permission="view",
             context=ShopRoot, route_name="kotti_eshop",
             renderer="kotti:templates/edit/node.pt")
class BackendProductAddForm(BaseFormView):
    """ A form view to instantiate a new BackendProduct
    """
    schema_factory = BackendProductSchema
    success_message = _(u"Product added.")

    def save_success(self, appstruct):
        appstruct.pop('csrf_token', None)
        product = BackendProduct(**appstruct)
        DBSession.add(product)
        self.request.session.flash(_(u"Product created."), 'success')
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root) +
                         '-shop/@@products')


class OrderStatusSchema(colander.MappingSchema):
    """ Schema for add and edit a possible order status
    """
    title = colander.SchemaNode(
        colander.String(),
        title=_(u'Title'),
    )
    description = colander.SchemaNode(
        colander.String(),
        title=_('Description'),
        widget=TextAreaWidget(cols=40, rows=5),
    )
    is_public = colander.SchemaNode(
        colander.Boolean(),
        title=_(u'Is public'),
        description=_(u'Public statuses are visible for the client, ' +
                      'private ones only for the admin.'),
    )


@view_config(name="add-order-status", permission="view",
             context=ShopRoot, route_name="kotti_eshop",
             renderer="kotti:templates/edit/node.pt")
class OrderStatusAddForm(BaseFormView):
    """ A form view to instantiate a new OrderStatus
    """
    schema_factory = OrderStatusSchema
    success_message = _(u"Status added.")

    def save_success(self, appstruct):
        appstruct.pop('csrf_token', None)
        status = OrderStatus(**appstruct)
        DBSession.add(status)
        self.request.session.flash(_(u"Status added."), 'success')
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root) +
                         '-shop/@@statuses')


@view_config(name="edit-order-status", permission="view",
             renderer="kotti:templates/edit/node.pt")
class OrderStatusEditForm(EditFormView):
    """ A form view to edit an OrderStatus
        Example: www.mykottisite.com/@@edit-order-status?status_id=3
    """
    schema_factory = OrderStatusSchema
    success_message = _(u"Status details saved.")
    first_heading = (u"Edit status details")

    @reify
    def success_url(self):
        root = get_root()
        return self.request.resource_url(root) + '-shop/@@statuses'

    def before(self, form):
        get = self.request.GET
        status_id = get.get('status_id', None)
        if status_id is not None:
            status = DBSession.query(OrderStatus).filter(
                OrderStatus.id == status_id).first()
            if status:
                form.appstruct = get_appstruct(self.context, self.schema)
                form.appstruct.update({
                    'title': status.title,
                    'description': status.description,
                    'is_public': status.is_public,
                })

    def edit(self, **appstruct):
        get = self.request.GET
        status_id = get.get('status_id', None)
        if status_id is not None:
            status = DBSession.query(OrderStatus).filter(
                OrderStatus.id == int(status_id)).first()
            if status:
                status.title = appstruct['title']
                status.description = appstruct['description']
                status.is_public = appstruct['is_public']
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root) +
                         '-shop/@@statuses')


@view_config(name="edit-product", permission="view",
             renderer="kotti:templates/edit/node.pt")
class BackendProductEditForm(EditFormView):
    """ A form view to edit a BackendProduct
        Example: www.mykottisite.com/@@edit-product?product_id=3
    """
    schema_factory = BackendProductSchema
    success_message = _(u"Product details saved.")
    first_heading = (u"Edit product details")

    @reify
    def success_url(self):
        root = get_root()
        return self.request.resource_url(root) + '-shop/@@products'

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
                    'is_active': product.is_active,
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
                         '-shop/@@products')


@view_config(name="edit-client", permission="view",
             renderer="kotti:templates/edit/node.pt")
class ShopClientEditForm(EditFormView):
    """ A form view to edit a ShopClient
        Example: www.mykottisite.com/@@edit-client?client_id=3
    """
    schema_factory = ShopClientSchema
    success_message = _(u"Client details saved.")
    first_heading = (u"Edit client details")

    @reify
    def success_url(self):
        root = get_root()
        return self.request.resource_url(root) + '-shop/@@clients'

    def before(self, form):
        get = self.request.GET
        client_id = get.get('client_id', None)
        if client_id is not None:
            client = DBSession.query(ShopClient).filter_by(
                id=client_id).first()
            if client:
                form.appstruct = get_appstruct(self.context, self.schema)
                form.appstruct.update({
                    'email': client.email,
                })

    def edit(self, **appstruct):
        get = self.request.GET
        client_id = get.get('client_id', None)
        if client_id is not None:
            client = DBSession.query(ShopClient).filter_by(
                id=client_id).first()
            if client:
                client.email = appstruct['email']
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root) +
                         '-shop/@@clients')


class PKType(colander.Integer):

    def __init__(self, model):
        self.model = model

    def deserialize(self, node, cstruct):
        return DBSession.query(self.model).get(int(cstruct))

    def serialize(self, node, cstruct):
        if cstruct is colander.null:
            return
        return str(cstruct.id)


class Products(colander.SequenceSchema):
    product = colander.SchemaNode(
        PKType(BackendProduct),
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
        self.request.session.flash(_(u"Product assigned."), 'success')
        return HTTPFound(location=self.request.resource_url(self.context))

    def before(self, form):
        selectize.need()
        return super(AssignBackendProductForm, self).before(form)


class ProductOperationSchema(colander.Schema):
    backend_product = colander.SchemaNode(
        PKType(BackendProduct)
    )


# def shop_admin_index(context, request):
#     if request.subpath:`


@view_config(name='shop_admin', permission="manage",
             renderer='kotti_eshop:templates/shop-admin-view.pt')
class AdminViews(BaseFormView):
    """ Shop administration panel
    """

    schema_factory = ProductOperationSchema
    use_csrf_token = False

    buttons = (
        deform.Button('delete_backend_product', _(u'Delete')),
        deform.Button('delete_product_assignment', _(u'Delete')),
        deform.Button('activate_backend_product', _(u'Activate')),
        deform.Button('deactivate_backend_product', _(u'Dectivate'))
    )

    def delete_backend_product_success(self, appstruct):
        product = appstruct['backend_product']
        if not product.assigned_to_content:  # avoid integrity error
            if not(product.shoppingcart_placements or
                   product.shoporders_placements):  # avoid AssertionError
                DBSession.delete(product)
                self.request.session.flash(_(u"Product deleted."), 'success')
            else:
                product.is_active = False
                self.request.session.flash(
                    _(u"Cannot be deleted because it is used in some " +
                      "carts or orders. Product deactivated."), 'info')
        else:
            self.request.session.flash(
                _(u"Cannot be deleted because it is assigned to some " +
                    "content. Delete product assignments first."), 'info')
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root) +
                         '-shop/@@products')

    def delete_product_assignment_success(self, appstruct):
        product = appstruct['backend_product']
        content_item_id = self.request.params.get('content_item_id', None)
        if product is not None and content_item_id is not None:
            for content in product.assigned_to_content:
                if content.id == int(content_item_id):
                    product.assigned_to_content.remove(content)
        self.request.session.flash(_(u"Assignment deleted."), 'success')
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root) +
                         '-shop/@@products')

    def deactivate_backend_product_success(self, appstruct):
        product = appstruct['backend_product']
        product.is_active = False
        self.request.session.flash(_(u"Product deactivated."), 'success')
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root) +
                         '-shop/@@products')

    def activate_backend_product_success(self, appstruct):
        product = appstruct['backend_product']
        product.is_active = True
        self.request.session.flash(_(u"Product activated."), 'success')
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root) +
                         '-shop/@@products')


@view_config(name="",  # permission="edit",
             route_name="kotti_eshop",
             renderer='kotti_eshop:templates/shop-admin-view.pt')
def view_shop_root(context, request):
    return {}


@view_config(name="products", context=ShopRoot, route_name="kotti_eshop",
             renderer="kotti_eshop:templates/shop-admin-products.pt")
def shop_admin_products(context, request):
    return {}


@view_config(name="clients", context=ShopRoot, route_name="kotti_eshop",
             renderer="kotti_eshop:templates/shop-admin-clients.pt")
def shop_admin_clients(context, request):
    return {}


@view_config(name="orders", context=ShopRoot, route_name="kotti_eshop",
             renderer="kotti_eshop:templates/shop-admin-orders.pt")
def shop_admin_orders(context, request):
    return {}


@view_config(name="statuses", context=ShopRoot, route_name="kotti_eshop",
             renderer="kotti_eshop:templates/shop-admin-statuses.pt")
def shop_admin_order_possible_statuses(context, request):
    return {}


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
                # CREATE cart
                if 'shoppingcart_uid' not in self.request.session:
                    shoppingcart_uid = str(uuid.uuid4())
                    cart = ShoppingCart(
                            shoppingcart_uid=shoppingcart_uid,
                            creation_date=datetime.today()
                        )
                    DBSession.add(cart)
                    self.request.session['shoppingcart_uid'] = shoppingcart_uid
                # GET cart
                else:
                    shoppingcart_uid = str(self.request.session.get(
                        'shoppingcart_uid'))
                    cart = DBSession.query(ShoppingCart).filter_by(
                        shoppingcart_uid=shoppingcart_uid).first()

                # ADD product
                cart.add_to_cart(product_id=int(product_id), quantity=quantity)
                self.request.session.flash(_(u"Added to cart."), 'success')

        # REMOVE from cart
        if 'remove_from_cart' in self.request.params:
            product_id = self.request.params.get('backend_product_id', None)
            if 'shoppingcart_uid' in self.request.session:
                shoppingcart_uid = str(
                    self.request.session['shoppingcart_uid'])
                cart = DBSession.query(ShoppingCart).filter_by(
                    shoppingcart_uid=shoppingcart_uid).first()
                cart.change_product_quantity(
                    product_id=int(product_id), delta=0)
                self.request.session.flash(_(u"Removed from cart."), 'success')
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root))


@view_config(
    name="assign-product-menu-entry", permission="edit",
    renderer="kotti_eshop:templates/edit/assign-product-menu-entry.pt")
def assign_product_menu_entry(context, request):
    return {}


class ShippingAddressSchema(colander.MappingSchema):
    """ Schema for ShippingAddress
    """
    recipient_fullname = colander.SchemaNode(
        colander.String(),
        title=_(u'Full Name'),
        description=_(u'Recipient full name'),
    )

    address_line1 = colander.SchemaNode(
        colander.String(),
        title=_(u'Address Line 1'),
        description=_(u'Street address, number, company name, etc.'),
    )

    address_line2 = colander.SchemaNode(
        colander.String(),
        title=_(u'Address Line 2'),
        description=_(u'Apartament, suite, unit, building, floor, etc.'),
    )

    city = colander.SchemaNode(
        colander.String(),
        title=_(u'City'),
        description=_(u'City / Locality'),
    )

    region = colander.SchemaNode(
        colander.String(),
        title=_(u'Region'),
        description=_(u'State / Province / Region'),
    )

    postal_code = colander.SchemaNode(
        colander.String(),
        title=_(u'Postal Code'),
        description=_(u'ZIP / Postal Code'),
    )

    country = colander.SchemaNode(
        colander.String(),
        title=_(u'Country'),
    )


@view_config(name='checkout', permission='view',
             renderer='kotti_eshop:templates/checkout.pt')
class CheckoutView(object):
    """ Checkout view (multiple forms)
    """
    def __init__(self, request):
        self.request = request

    def __call__(self):
        import itertools

        counter = itertools.count()

        shop_client_schema = ShopClientSchema()
        form_client = deform.Form(
            shop_client_schema, buttons=('submit',),
            formid='form_client', counter=counter)

        shipping_address_schema = ShippingAddressSchema()
        form_address = deform.Form(
            shipping_address_schema, buttons=('submit',),
            formid='form_address', counter=counter)

        html = []
        captured = None
        form_validation_errors = False

        if 'submit' in self.request.POST:
            posted_formid = self.request.POST['__formid__']

            # SUBMIT client
            if posted_formid == "form_client":
                try:
                    controls = self.request.POST.items()
                    captured = form_client.validate(controls)
                    html.append(form_address.render())  # address is next step
                except deform.ValidationFailure as e:
                    html.append(e.render())
                    form_validation_errors = True
                if not form_validation_errors:
                    # GET or CREATE client and assign this shopping cart
                    email = captured.get('email')
                    shoppingcart_uid = str(
                        self.request.session.get('shoppingcart_uid'))
                    cart = DBSession.query(ShoppingCart).filter_by(
                        shoppingcart_uid=shoppingcart_uid).first()
                    client = DBSession.query(ShopClient).filter_by(
                        email=email).first()
                    if client:
                        client.shopping_cart = []
                    else:
                        client = ShopClient(
                            email=email, creation_date=datetime.today())
                    cart.client.append(client)
                    progress_value = 80
                    progress_status = _(u'Select address. Finish order.')
            # SUBMIT address
            elif posted_formid == "form_address":
                try:
                    controls = self.request.POST.items()
                    captured = form_address.validate(controls)
                except deform.ValidationFailure as e:
                    html.append(e.render())
                    form_validation_errors = True
                if not form_validation_errors:
                    shoppingcart_uid = str(
                        self.request.session.get('shoppingcart_uid'))
                    cart = DBSession.query(ShoppingCart).filter_by(
                        shoppingcart_uid=shoppingcart_uid).first()
                    client = cart.client[0]

                    shipping_address = client.get_shipping_address(
                        recipient_fullname=captured.get('recipient_fullname'),
                        address_line1=captured.get('address_line1'),
                        address_line2=captured.get('address_line2'),
                        city=captured.get('city'),
                        region=captured.get('region'),
                        postal_code=captured.get('postal_code'),
                        country=captured.get('country'))

                    if shipping_address is None:
                        shipping_address = ShippingAddress(
                            recipient_fullname=captured.get(
                                'recipient_fullname'),
                            address_line1=captured.get('address_line1'),
                            address_line2=captured.get('address_line2'),
                            city=captured.get('city'),
                            region=captured.get('region'),
                            postal_code=captured.get('postal_code'),
                            country=captured.get('country'),
                            creation_date=datetime.today())
                        client.shipping_addresses.append(shipping_address)

                    order = ShopOrder(creation_date=datetime.today())
                    order.shipping_address.append(shipping_address)
                    client.shop_orders.append(order)
                    order.save_content_from_cart(cart)

                    # Reset cart. Else there can be a problem with
                    # client = cart.client[0] if two different clients
                    # will use the same cart in a session.
                    # [TODO] Fix delete cart from db without
                    # AssertionError: Dependency rule tried to blank-out
                    # primary key column
                    # for multiple products in cart
                    del self.request.session['shoppingcart_uid']

                    root = get_root()
                    self.request.session.flash(_(
                        u"Order finished. Check your email for " +
                        "notifications."), 'success')
                    return HTTPFound(location=self.request.resource_url(root))
        else:
            # NO SUBMIT - go to first step: select client
            html.append(form_client.render())
            progress_value = 40
            progress_status = _(u'Selecting account.')

        html = ''.join(html)

        return {
            'form': html,
            'progress_value': progress_value,
            'progress_status': progress_status
        }
