from kotti.resources import Base
from kotti.resources import Content
from kotti.resources import DBSession
from kotti.views.util import TemplateAPI as BaseTemplateAPI
from kotti_settings.util import get_setting
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

    assigned_content = relationship(Content,
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

    products = relationship("ProductCartPlacement", backref="shopping_cart")

    def __init__(self, **kw):
        super(ShoppingCart, self).__init__(**kw)
        self.__dict__.update(kw)


class ProductCartPlacement(Base):
    __tablename__ = 'shopping_carts_to_products_association'
    shopping_cart_id = Column(Integer, ForeignKey('shopping_carts.id'),
                              primary_key=True)
    product_id = Column(Integer, ForeignKey('backend_products.id'),
                        primary_key=True)
    quantity = Integer()
    products = relationship("BackendProduct", backref="shopping_carts")
