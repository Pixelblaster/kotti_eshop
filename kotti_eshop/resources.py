# -*- coding: utf-8 -*-
from datetime import date
from kotti_eshop import _
from kotti_eshop.utils import string_to_list
from kotti.resources import Content
from kotti.resources import DBSession
from kotti.resources import Image
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String


def get_all_clients():
    """ Returns all shop clients """
    clients = DBSession.query(ShopClient)
    return clients


def get_all_products():
    """ Returns all shop products """
    products = DBSession.query(ShopProduct)
    return products


def get_featured_products():
    """ Returns all featured products """
    featured_products = DBSession.query(ShopProduct)
    return featured_products


def remove_product_from_cart(self, id_client, id_product, quantity=0):
    """ Remove a quantity of this product from client's shopping cart

        quantity=0 means remove all quantity for
        and sure you will prefer to use it like this:
        shop.remove_product_from_cart(id_client=cid, id_product=pid)
    """
    # GET client
    clients = DBSession.query(ShopClient).filter(
        ShopClient.id == id_client)
    if clients.count() > 0:
        client = clients.first()

        # GET product
        products = DBSession.query(ShopProduct).filter(
            ShopProduct.id == id_product)
        if products.count() > 0:
            product = products.first()

            # Client and product exists. Get cart content:
            shopping_cart_list = string_to_list(client.shopping_cart)

            product_in_cart = False
            remove_product = False
            for p in shopping_cart_list:
                if p['product_id'] == product.id:
                    product_in_cart = True

                    # CHECK quantity
                    if (p['product_quantity'] > quantity
                            and quantity != 0):
                        # REMOVE given quantity
                        p['product_quantity'] -= quantity
                        message = _("Quantity removed for this product.")
                    else:
                        remove_product = True
            if remove_product:
                # REMOVE PRODUCT
                shopping_cart_list[:] = [
                    d for d in shopping_cart_list
                    if d.get('product_id') != product.id]
                message = _("Product removed from cart.")

            # UPDATE cart and product quantity in shop
            client.shopping_cart = str(shopping_cart_list)
            product.quantity = product.quantity + quantity

            if product_in_cart is False:
                message = _("Product not in cart.")
        else:
            message = _("Product not in database.")
    else:
        message = _("Client missing.")
    return message


def add_product_to_cart(self, id_client, id_product, quantity=1):
    """ Add a product to a client cart
    """
    # GET client
    clients = DBSession.query(ShopClient).filter(
        ShopClient.id == id_client)
    if clients.count() > 0:
        client = clients.first()

        # GET product
        products = DBSession.query(ShopProduct).filter(
            ShopProduct.id == id_product)
        if products.count() > 0:
            product = products.first()

            # Client and product exists. Get old cart content:
            shopping_cart_list = string_to_list(client.shopping_cart)

            # CHECK if quantity is available
            if quantity <= product.quantity:
                record = {'product_id': product.id,
                          'product_quantity': quantity}

                product_already_in_cart = False
                for p in shopping_cart_list:
                    if p['product_id'] == product.id:
                        # MERGE quantities
                        p['product_quantity'] += quantity
                        product_already_in_cart = True

                if product_already_in_cart is False:
                    # or ADD product to cart
                    shopping_cart_list.append(record)

                # MOVE records form shop to cart
                client.shopping_cart = str(shopping_cart_list)
                product.quantity = product.quantity - quantity
                message = _("Product added to cart.")
            else:
                message = _("Not enough quantity.")
        else:
            message = _("Product missing.")
    else:
        message = _("Client missing.")

    return message


def get_shopping_cart(self, id_client):
    """ Get cart for a given client in this shop
    """
    clients = DBSession.query(ShopClient).filter(
        ShopClient.id == id_client)
    if clients.count() > 0:
        client = clients.first()
        shopping_cart_list = string_to_list(client.shopping_cart)

    cart_content = []
    for product in shopping_cart_list:
        product_id = product.get('product_id', 0)
        product_quantity = product.get('product_quantity', 0)
        products = DBSession.query(ShopProduct).filter(
            ShopProduct.id == product_id)
        if products.count() > 0:
            # product exists in database
            product = products.first()
            record = (product, product_quantity)
            cart_content.append(record)
    return cart_content


def add_product_to_wishlist(self, id_client, id_product):
    """ Add a product to a client wishlist
    """
    # GET client
    clients = DBSession.query(ShopClient).filter(
        ShopClient.id == id_client)
    if clients.count() > 0:
        client = clients.first()

        # GET product
        products = DBSession.query(ShopProduct).filter(
            ShopProduct.id == id_product)
        if products.count() > 0:
            product = products.first()

            # GET wishlist
            wishlist = string_to_list(client.wishlist)
            if product.id not in wishlist:
                wishlist.append(product.id)
                client.wishlist = str(wishlist)
                message = _("Product added to wishlist.")
            else:
                message = _("Product already in wishlist.")
        else:
            message = _("Product not in database.")
    else:
        message = _("Client not in database.")

    return message


def remove_product_from_wishlist(self, id_client, id_product):
    """ Remove a product from a client wishlist
    """
    # GET client
    clients = DBSession.query(ShopClient).filter(
        ShopClient.id == id_client)
    if clients.count() > 0:
        client = clients.first()

        # GET product
        products = DBSession.query(ShopProduct).filter(
            ShopProduct.id == id_product)
        if products.count() > 0:
            product = products.first()

            # GET wishlist
            wishlist = string_to_list(client.wishlist)
            if product.id in wishlist:
                wishlist = [product_id for product_id in wishlist if
                            product_id != product.id]
                client.wishlist = str(wishlist)
                message = _("Product removed from wishlist.")
            else:
                message = _("Product not in wishlist.")
        else:
            message = _("Product not in database.")
    else:
        message = _("Client not in database.")

    return message


def get_wishlist(self, id_client):
    """ Get wishlist for a given client in this shop
    """
    # GET client
    clients = DBSession.query(ShopClient).filter(
        ShopClient.id == id_client)
    if clients.count() > 0:
        client = clients.first()

        # GET wishlist
        wishlist = string_to_list(client.wishlist)

    wishlist_products = []
    for product_id in wishlist:
        products = DBSession.query(ShopProduct).filter(
            ShopProduct.id == product_id)
        if products.count() > 0:
            # product exists in database
            product = products.first()
            wishlist_products.append(product)
    return wishlist_products


class ShopOrder(Content):
    """ An order in eShop
    """
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)
    # id_user -> who is the client
    # id_product or list of products?
    # id_coupon - maybe was a special offer?
    # paymethod - paypal or something
    # currency
    # amount decimal(14,3)
    # ip_address
    # pay_date
    # support_date
    # status
    # notes
    type_info = Content.type_info.copy(
        name=u'ShopOrder',
        title=_(u'ShopOrder'),
        add_view=u'add_order',
        addable_to=['Shop', ],)


class ShopClient(Content):
    """ A client for this eShop
    """
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)
    shopping_cart = Column(String())    # Example:
    # [
    #     {'product_id' : 3, 'product_quantity' : 2},
    #     {'product_id' : 6, 'product_quantity' : 5}
    # ]
    wishlist = Column(String())    # Example: [1, 2, 3] - list of products ids
    nickname = Column(String())
    fullname = Column(String())
    email = Column(String())
    paypal_email = Column(String())
    deliver_address = Column(String())
    status = Column(String())
    last_ip_login = Column(String())
    type_info = Content.type_info.copy(
        name=u'ShopClient',
        title=_(u'ShopClient'),
        add_view=u'add_client',
        addable_to=['Shop', ],)


class ShopProduct(Content):
    """ A product in this eShop
    """
    __tablename__ = 'shopproduct'

    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)
    price = Column(Float())
    price_offer = Column(Float())
    expires_offer_date = Column(Date())
    support_days = Column(Integer())
    featured = Column(Boolean())
    quantity = Column(Integer())

    type_info = Content.type_info.copy(
        name=u'ShopProduct',
        title=_(u'ShopProduct'),
        add_view=u'add_product',
        addable_to=['Shop', ],)

    def __init__(self, **kwargs):
        super(ShopProduct, self).__init__(**kwargs)

        for attr in ['materials', 'categories', 'topics', 'ages']:
            val = kwargs.get(attr)
            if val:
                setattr(self, attr, val)

    def get_all_images(self):
        """ Returns all images added to this product """
        images = DBSession.query(Image).filter(
            Image.parent_id == self.id)

        return images

    def quantity_status(self):
        """ Returns quantity status for this product based on quantity
            and the setting in shop settings
        """
        product = self
        shop = product.parent
        limited_quantity_number = shop.shop_products_limited_quantity()
        if product.quantity > limited_quantity_number:
            status = _("Available")
        else:
            if product.quantity > 0:
                status = _("Limited")
            else:
                status = _("Not available")

        return status

    def has_price_offer(self):
        """ Check if this product has price offer
        """
        product = self
        today = date.today()
        if product.price_offer and product.expires_offer_date >= today:
            return True
        else:
            return False

    def final_price(self):
        """ Returns final price for this product
        """
        product = self
        if product.has_price_offer():
            return product.price_offer
        else:
            return product.price
