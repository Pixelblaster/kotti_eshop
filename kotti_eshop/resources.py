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


    # def get_all_images(self):
    #     """ Returns all images added to this product """
    #     images = DBSession.query(Image).filter(
    #         Image.parent_id == self.id)
    #
    #     return images
    #
    # def has_price_offer(self):
    #     """ Check if this product has price offer
    #     """
    #     product = self
    #     today = date.today()
    #     if product.price_offer and product.expires_offer_date >= today:
    #         return True
    #     else:
    #         return False
    #
    # def final_price(self):
    #     """ Returns final price for this product
    #     """
    #     product = self
    #     if product.has_price_offer():
    #         return product.price_offer
    #     else:
    #         return product.price
