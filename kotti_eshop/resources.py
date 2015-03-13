# -*- coding: utf-8 -*-
from datetime import date
from kotti_eshop import _
from kotti.resources import Content
from kotti.resources import DBSession
from kotti.resources import Image
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer


def get_all_products():
    """ Returns all shop products """
    products = DBSession.query(ShopProduct)
    return products


class ShopProduct(Content):
    """ A product in this eShop
    """
    __tablename__ = 'shopproduct'

    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)
    price = Column(Float())
    price_offer = Column(Float())
    expires_offer_date = Column(Date())
    support_days = Column(Integer())

    type_info = Content.type_info.copy(
        name=u'ShopProduct',
        title=_(u'ShopProduct'),
        add_view=u'add_product',
        addable_to=['Shop', ],)

    def __init__(self, **kwargs):
        super(ShopProduct, self).__init__(**kwargs)

    def get_all_images(self):
        """ Returns all images added to this product """
        images = DBSession.query(Image).filter(
            Image.parent_id == self.id)

        return images

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

from kotti.resources import Content, Link

Content.type_info.edit_links.append(Link("edit-as-product", "Edit as Product"))
