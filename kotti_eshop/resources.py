from kotti.resources import Base
from kotti.resources import Content
from kotti.resources import DBSession
from kotti.views.util import TemplateAPI as BaseTemplateAPI
from kotti_settings.util import get_setting
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import Unicode
from sqlalchemy.orm import relationship


class TemplateAPI(BaseTemplateAPI):

    def shop_currency(self):
        """ Returns shop currency (ex: USD)
            from kotti_settings
        """
        return get_setting('shop_currency')

    def get_all_backend_products(self):
        """ Returns all backend products
        """
        products = DBSession.query(BackendProduct).order_by(
            BackendProduct.created)
        return products

    def get_all_clients(self):
        """ Returns all shop clients
        """
        clients = DBSession.query(ShopClient).order_by(
            ShopClient.creation_date)
        return clients

    def get_all_orders(self):
        """ Returns all orders
        """
        orders = DBSession.query(ShopOrder).order_by(
            ShopOrder.creation_date)
        return orders

    def get_all_possible_order_statuses(self):
        """ Returns all possible order order statuses for this shop
        """
        statuses = DBSession.query(OrderStatus).order_by(
            OrderStatus.creation_date)
        return statuses

    def get_backend_product(self, product_id):
        """ Get backend product by id
        """
        product = DBSession.query(BackendProduct).filter(
            BackendProduct.id == product_id)
        return product

product_association_table = Table(
    'contents_to_products', Base.metadata,
    Column('backendproduct_id', Integer(), ForeignKey('backend_products.id')),
    Column('contents_id', Integer(), ForeignKey('contents.id')),
)

client_cart_association_table = Table(
    'clients_to_carts', Base.metadata,
    Column('shopclient_id', Integer(), ForeignKey('shop_clients.id')),
    Column('shoppingcart_id', Integer(), ForeignKey('shopping_carts.id')),
)

client_addresses_association_table = Table(
    'clients_to_addresses', Base.metadata,
    Column('shopclient_id', Integer(), ForeignKey('shop_clients.id')),
    Column('shipping_address_id', Integer(),
           ForeignKey('shipping_addresses.id')),
)

client_orders_association_table = Table(
    'clients_to_orders', Base.metadata,
    Column('shopclient_id', Integer(), ForeignKey('shop_clients.id')),
    Column('shoporder_id', Integer(), ForeignKey('shop_orders.id')),
)

order_addresses_association_table = Table(
    'order_to_addresses', Base.metadata,
    Column('shoporder_id', Integer(), ForeignKey('shop_orders.id')),
    Column('shipping_address_id', Integer(),
           ForeignKey('shipping_addresses.id')),
)

order_statuses_association_table = Table(
    'order_to_statuses', Base.metadata,
    Column('shoporder_id', Integer(), ForeignKey('shop_orders.id')),
    Column('orderstatus_id', Integer(),
           ForeignKey('order_statuses.id')),
)


class BackendProduct(Base):
    """ A backend product in this eShop

    This is the simplest product definition. It is meant to be linked, from
    the front-end, to any document or page of the Kotti website and make those
    "the real products".

    """
    __tablename__ = 'backend_products'

    id = Column(Integer(), primary_key=True)
    pin = Column(Unicode(512))  # product identification number
    title = Column(Unicode(512), index=True)
    description = Column(Unicode())
    text = Column(Unicode())
    price = Column(Float(asdecimal=True))
    created = Column(DateTime())
    is_active = Column(Boolean, default=True)
    assigned_to_content = relationship(Content,
                                       backref="backend_products",
                                       secondary=product_association_table)

    def __init__(self, **kw):
        super(BackendProduct, self).__init__(**kw)
        self.__dict__.update(kw)


class ShoppingCart(Base):
    """ A shopping cart in this eShop
    """
    __tablename__ = 'shopping_carts'

    id = Column(Integer(), primary_key=True)
    shoppingcart_uid = Column(Unicode(512))
    creation_date = Column(DateTime())  # a shopping cart can live 30 days

    client = relationship("ShopClient", backref="shopping_cart",
                          secondary=client_cart_association_table)

    def __init__(self, **kw):
        super(ShoppingCart, self).__init__(**kw)
        self.__dict__.update(kw)

    def get_content_record(self, product_id=None):
        """ Get content record for a given product id
        """
        content_record = DBSession.query(ProductCartPlacement).filter(
            ProductCartPlacement.shopping_cart_id == self.id,
            ProductCartPlacement.product_id == product_id).first()
        return content_record

    def add_to_cart(self, product_id=None, quantity=1):
        """ Add product to cart
        """
        product = DBSession.query(BackendProduct).get(product_id)
        content_record = self.get_content_record(product_id=product_id)
        if content_record:
            self.change_product_quantity(product_id=product_id, delta=quantity)
        else:
            pcp = ProductCartPlacement(shopping_cart=self, product=product,
                                       quantity=quantity)
            DBSession.add(pcp)

    def get_total_price(self):
        """ Get total price for all products in cart
        """
        total = 0
        for content_record in self.cart_content:
            unit_price = content_record.product.price
            quantity = content_record.quantity
            total += unit_price * quantity
        return float(total)

    def change_product_quantity(self, product_id=None, delta=None):
        """ Change quantity for given product in this cart
            * delta=0 means you want to delete all quantity
        """
        if product_id is not None and delta is not None:
            content_record = self.get_content_record(product_id=product_id)
            if content_record:
                if delta != 0:
                    content_record.quantity += delta
                else:
                    DBSession.delete(content_record)


class ProductCartPlacement(Base):
    """ What products in what carts, in what quantity
    """
    __tablename__ = 'shopping_carts_to_products_association'

    shopping_cart_id = Column(Integer, ForeignKey('shopping_carts.id'),
                              primary_key=True)
    product_id = Column(Integer, ForeignKey('backend_products.id'),
                        primary_key=True)

    quantity = Column(Integer())

    product = relationship(BackendProduct,
                           backref="shoppingcart_placements")
    shopping_cart = relationship(ShoppingCart,
                                 backref="cart_content")

    def __init__(self, shopping_cart=None, product=None, quantity=None):
        super(ProductCartPlacement, self).__init__()

        if shopping_cart is not None:
            self.shopping_cart = shopping_cart

        if product is not None:
            self.product = product

        if quantity is not None:
            self.quantity = quantity


class ShopClient(Base):
    """ A client in this eShop
    """
    __tablename__ = 'shop_clients'
    id = Column(Integer(), primary_key=True)
    email = Column(Unicode(254))
    creation_date = Column(DateTime())

    shipping_addresses = relationship(
        "ShippingAddress", backref="client",
        secondary=client_addresses_association_table)

    shop_orders = relationship(
        "ShopOrder", backref="client",
        secondary=client_orders_association_table)

    def get_shipping_address(self, recipient_fullname=None, address_line1=None,
                             address_line2=None, city=None, region=None,
                             postal_code=None, country=None):
        """ Check if this client has a given address
        """
        client = self
        found_address = None
        for address in client.shipping_addresses:
            if (address.recipient_fullname == recipient_fullname and
                address.address_line1 == address_line1 and
                address.address_line2 == address_line2 and
                address.city == city and
                address.region == region and
                address.postal_code == postal_code and
                    address.country == country):
                found_address = address
        return found_address


class ShippingAddress(Base):
    """ A shipping address used by a shop client
    """
    __tablename__ = 'shipping_addresses'
    id = Column(Integer(), primary_key=True)
    creation_date = Column(DateTime())
    recipient_fullname = Column(Unicode())
    address_line1 = Column(Unicode())
    address_line2 = Column(Unicode())
    city = Column(Unicode())
    region = Column(Unicode())
    postal_code = Column(Unicode())
    country = Column(Unicode())


class ShopOrder(Base):
    """ An order in shop for a client
    """
    __tablename__ = 'shop_orders'
    id = Column(Integer(), primary_key=True)
    creation_date = Column(DateTime())

    @property
    def total_price(self):
        """ Total price for this order based on original unit price
            of each product
        """
        order_total_price = 0
        for p_o_p in self.order_content:
            order_total_price += p_o_p.original_unit_price * p_o_p.quantity
        return order_total_price

    shipping_address = relationship(
        "ShippingAddress", backref="order",
        secondary=order_addresses_association_table)

    status = relationship(
        "OrderStatus", backref="order",
        secondary=order_statuses_association_table)

    def save_content_from_cart(self, cart=None):
        """ The products are moved from cart to order saving the original price
            for each product
        """
        order = self
        if cart:
            for p_c_p in cart.cart_content:
                p_o_p = ProductOrderPlacement(
                        shop_order=order,
                        product=p_c_p.product,
                        quantity=p_c_p.quantity,
                        original_unit_price=p_c_p.product.price,
                    )
                DBSession.add(p_o_p)
                DBSession.delete(p_c_p)


class ProductOrderPlacement(Base):
    """ What products in what orders, in what quantity + original unit price
    """
    __tablename__ = 'orders_to_products_association'

    order_id = Column(Integer, ForeignKey('shop_orders.id'),
                      primary_key=True)
    product_id = Column(Integer, ForeignKey('backend_products.id'),
                        primary_key=True)

    quantity = Column(Integer())
    original_unit_price = Column(Float(asdecimal=True))

    product = relationship(BackendProduct,
                           backref="shoporders_placements")
    shop_order = relationship(ShopOrder, backref="order_content")

    def __init__(self, shop_order=None, product=None, quantity=None,
                 original_unit_price=None):
        super(ProductOrderPlacement, self).__init__()

        if shop_order is not None:
            self.shop_order = shop_order

        if product is not None:
            self.product = product

        if quantity is not None:
            self.quantity = quantity

        if original_unit_price is not None:
            self.original_unit_price = original_unit_price


class OrderStatus(Base):
    """ A status for an order
        Examples: payment accepted, preparation in progress, shipped,
                  delivered, canceled, refund, payment error,
                  awainting paypal payment

        Useful for shop admin and good for email notifications to client.
    """
    __tablename__ = 'order_statuses'
    id = Column(Integer(), primary_key=True)
    title = Column(Unicode())
    description = Column(Unicode())
    creation_date = Column(DateTime())
