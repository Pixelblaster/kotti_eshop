from datetime import datetime
from deform.widget import HiddenWidget
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


# class CameFromSchema(colander.Schema):
#     came_from = colander.SchemaNode(
#         colander.String(),
#         widget=HiddenWidget(),
#         default='',
#     )


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
             context=ShopRoot, route_name="kotti_eshop",
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
        deform.Button('delete_product_assignment', _(u'Delete'))
    )

    def delete_backend_product_success(self, appstruct):
        product = appstruct['backend_product']
        if not product.assigned_to_content:  # avoid integrity error
            DBSession.delete(product)
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root) +
                         '@@shop_admin?action=products')

    def delete_product_assignment_success(self, appstruct):
        product = appstruct['product']
        import pdb; pdb.set_trace()
        # product_id = self.request.params.get('backend_product_id', None)
        # content_item_id = self.request.params.get('content_item_id', None)
        # if product_id is not None and content_item_id is not None:
        #     product = DBSession.query(BackendProduct).filter(
        #         BackendProduct.id == product_id).first()
        #     if product:
        #         for content in product.assigned_content:
        #             if content.id == int(content_item_id):
        #                 product.assigned_content.remove(content)
        #
        #         root = get_root()
        #         return HTTPFound(location=self.request.resource_url(root) +
        #                          '@@shop_admin?action=products')


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

        root = get_root()
        return HTTPFound(location=self.request.resource_url(root))


@view_config(
    name="assign-product-menu-entry", permission="edit",
    renderer="kotti_eshop:templates/edit/assign-product-menu-entry.pt")
def assign_product_menu_entry(context, request):
    return {}


class CheckoutSchema(colander.MappingSchema):
    """ Schema for Checkout form
    """
    email = colander.SchemaNode(
        colander.String(),
        title=_(u'Email'),
        description=_(u'To receive notifications about your order.'),
    )

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
class CheckoutView(BaseFormView):
    """ Checkout view
    """

    schema_factory = CheckoutSchema
    buttons = ('finish', 'back')
    success_message = _(u"Order finished. Check your email for notifications.")

    def first_heading(self):
        return _(u"Enter details:")

    def form_description(self):
        return _(u"Form description")

    def finish_success(self, appstruct):
        email = appstruct['email']

        shoppingcart_uid = str(self.request.session.get('shoppingcart_uid'))
        cart = DBSession.query(ShoppingCart).filter_by(
            shoppingcart_uid=shoppingcart_uid).first()

        client = DBSession.query(ShopClient).filter_by(email=email).first()
        if client:
            client.shopping_cart = []
            cart.client.append(client)
        else:
            client = ShopClient(email=email, creation_date=datetime.today())
            cart.client.append(client)

        shipping_address = ShippingAddress(
            recipient_fullname=appstruct['recipient_fullname'],
            address_line1=appstruct['address_line1'],
            address_line2=appstruct['address_line2'],
            city=appstruct['city'],
            region=appstruct['region'],
            postal_code=appstruct['postal_code'],
            country=appstruct['country'],
            creation_date=datetime.today())

        client.shipping_addresses.append(shipping_address)

        order = ShopOrder(creation_date=datetime.today())

        order.shipping_address.append(shipping_address)
        client.shop_orders.append(order)

        order.save_content_from_cart(cart)

        root = get_root()
        self.request.session.flash(self.success_message, 'success')
        return HTTPFound(location=self.request.resource_url(root))

    def back_success(self, appstruct):
        root = get_root()
        return HTTPFound(location=self.request.resource_url(root))


@view_config(name='multiple_forms', permission='view',
             renderer='kotti_eshop:templates/checkout.pt')
class CheckoutViewMultipleForms(object):
    """ Checkout view with multiple forms
    """
    def __init__(self, request):
        self.request = request

    def __call__(self):
        import itertools

        counter = itertools.count()

        class Schema1(colander.Schema):
            name1 = colander.SchemaNode(colander.String())
        schema1 = Schema1()
        form1 = deform.Form(schema1, buttons=('submit',), formid='form1',
                            counter=counter)

        class Schema2(colander.Schema):
            name2 = colander.SchemaNode(colander.String())
        schema2 = Schema2()
        form2 = deform.Form(schema2, buttons=('submit',), formid='form2',
                            counter=counter)

        html = []
        captured = None

        if 'submit' in self.request.POST:
            posted_formid = self.request.POST['__formid__']
            for (formid, form) in [('form1', form1), ('form2', form2)]:
                if formid == posted_formid:
                    try:
                        controls = self.request.POST.items()
                        captured = form.validate(controls)
                        html.append(form.render(captured))
                    except deform.ValidationFailure as e:
                        # the submitted values could not be validated
                        html.append(e.render())
                else:
                    html.append(form.render())
        else:
            for form in form1, form2:
                html.append(form.render())

        html = ''.join(html)

        # code, start, end = self.get_code(1)

        # values passed to template for rendering
        return {
            'form': html,
            'captured': repr(captured),
            # 'code': code,
            # 'start': start,
            # 'demos': self.get_demos(),
            # 'end': end,
            'title': 'Multiple Forms on the Same Page',
            }
