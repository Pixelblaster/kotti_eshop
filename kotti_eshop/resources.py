# -*- coding: utf-8 -*-

from kotti.interfaces import IDefaultWorkflow
from kotti.resources import Content
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from zope.interface import implements

from kotti_eshop import _


class Shop(Content):
    """ An eShop in this website
    """
    id = Column(Integer(), ForeignKey('contents.id'), primary_key=True)

    type_info = Content.type_info.copy(
        name=u'Shop',
        title=_(u'Shop'),
        add_view=u'add_shop',
        addable_to=['Document', ],)


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
    # email
    # paypal_email
    # deliver_address
    # status
    # last_ip_login
    type_info = Content.type_info.copy(
        name=u'ShopClient',
        title=_(u'ShopClient'),
        add_view=u'add_client',
        addable_to=['Shop', ],)


class CustomContent(Content):
    """ A custom content type. """

    implements(IDefaultWorkflow)

    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    custom_attribute = Column(Unicode(1000))

    type_info = Content.type_info.copy(
        name=u'CustomContent',
        title=_(u'CustomContent'),
        add_view=u'add_custom_content',
        addable_to=[u'Document'],
        selectable_default_views=[
            ("alternative-view", _(u"Alternative view")),
        ],
    )

    def __init__(self, custom_attribute=None, **kwargs):
        """ Constructor

        :param custom_attribute: A very custom attribute
        :type custom_attribute: unicode

        :param **kwargs: Arguments that are passed to the base class(es)
        :type **kwargs: see :class:`kotti.resources.Content`
        """

        super(CustomContent, self).__init__(**kwargs)

        self.custom_attribute = custom_attribute
