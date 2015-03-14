# -*- coding: utf-8 -*-

from datetime import date
from kotti.resources import Base
from kotti.resources import Content
from kotti.resources import Link
from kotti.resources import DBSession
from kotti.resources import Image
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Unicode
#from sqlalchemy import ForeignKey
from sqlalchemy import Integer


class ShopProduct(Base):
    """ A product in this eShop
    """
    __tablename__ = 'kotti_eshop_products'

    id = Column(Integer(), primary_key=True)
    title = Column(Unicode(512), index=True)
    description = Column(Unicode())
    price = Column(Float(asdecimal=True))
    created = Column(DateTime())

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

Content.type_info.edit_links.append(Link("assign-product",
                                         _("Assign a product")))
