# -*- coding: utf-8 -*-
import colander
from colander import SequenceSchema
from colander import Schema
from colander import SchemaNode
from colander import String
from deform.widget import SelectWidget
from kotti_eshop import _
from kotti_eshop.fanstatic import selectize
from kotti_eshop.resources import Shop
from kotti_eshop.resources import ShopClient
from kotti_eshop.resources import ShopProduct
from kotti_eshop.resources import ProductAge
from kotti_eshop.resources import ProductCategory
from kotti_eshop.resources import ProductMaterial
from kotti_eshop.resources import ProductTopic
from kotti.resources import DBSession
from kotti.views.edit import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.view import view_config


class ProductCategories(SequenceSchema):
    productcategory = SchemaNode(String(), title=_("productcategory"))


class ProductMaterials(SequenceSchema):
    productmaterial = SchemaNode(String(), title=_("productmaterial"))


class ProductTopics(SequenceSchema):
    producttopic = SchemaNode(String(), title=_("producttopic"))


class ProductAges(SequenceSchema):
    productage = SchemaNode(String(), title=_("productage"))


class ShopSchema(ContentSchema):
    """ Schema for Shop. """


def ShopProductSchema(title_missing=None):
    class ShopProductSchema(ContentSchema):
        price = colander.SchemaNode(
            colander.Float(),
            title=_(u"Price"),
            description=_(u"The price for this product"))

        support_days = colander.SchemaNode(
            colander.Integer(),
            title=_(u"Support days"),
            description=_(u"Number of support days for this product"))

        featured = colander.SchemaNode(
            colander.Boolean(),
            title=_(u"Featured"),
            description=_(u"Do you want this product to be featured?"))

        quantity = colander.SchemaNode(
            colander.Integer(),
            title=_(u"Quantity"),
            description=_(u"How many items of this product are in your shop?"))

        productmaterials = ProductMaterials(
            widget=get_selectize_widget(ProductMaterial),
            title=_(u"Materials"),
            description=_("Type or select materials"))

        productcategories = ProductCategories(
            widget=get_selectize_widget(ProductCategory),
            title=_(u"Categories"),
            description=_("Type or select categories"))

        producttopics = ProductTopics(
            widget=get_selectize_widget(ProductTopic),
            title=_(u"Topics"),
            description=_("Type or select topics"))

        productages = ProductAges(
            widget=get_selectize_widget(ProductAge),
            title=_(u"Ages"),
            description=_("Type or select ages"))

    return ShopProductSchema()


class ShopProductPriceOfferSchema(Schema):
    price = colander.SchemaNode(
        colander.Float(),
        title=_(u"Price"),
        description=_(u"The price for this product"))

    price_offer = colander.SchemaNode(
        colander.Float(),
        title=_(u"Price offer"),
        description=_(u"A better price for a time period"))

    expires_offer_date = colander.SchemaNode(
        colander.Date(),
        title=_(u"Date"),
        description=_(u"The date for offer time period end"))


class ShopClientSchema(Schema):
    name = colander.SchemaNode(
        colander.String(),
        title=_(u"Nickname"),
        description=_(u"Your nickname in this shop"))

    title = colander.SchemaNode(
        colander.String(),
        title=_(u"Full name"),
        description=_(u"Your full name. This is important."))

    email = colander.SchemaNode(
        colander.String(),
        title=_(u"Email"),
        description=_(u"Your email"))

    paypal_email = colander.SchemaNode(
        colander.String(),
        title=_(u"Your paypal email"),
        description=_(u"Only if you want to use a paypal account"))

    deliver_address = colander.SchemaNode(
        colander.String(),
        title=_(u"Your deliver address"),
        description=_(u"Our products will go there"))


class ShopSelectizeWidget(SelectWidget):

    template = "kotti_eshop:templates/selectize.pt"
    multiple = True
    css_class = 'selectize'


def get_selectize_widget(factory):
    @colander.deferred
    def widget(node, kw):
        values = [(v[0], v[0])
                  for v in sorted(DBSession.query(factory.title).all())]
        return ShopSelectizeWidget(values=values)

    return widget


@view_config(name=Shop.type_info.add_view, permission='add',
             renderer='kotti:templates/edit/node.pt')
class ShopAddForm(AddFormView):
    """ Form to add a new Shop. """

    schema_factory = ShopSchema
    add = Shop
    item_type = _(u"Shop")


@view_config(name='edit', context=Shop, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class ShopEditForm(EditFormView):
    """ Form to edit existing Shop objects. """

    schema_factory = ShopSchema


@view_config(name=ShopProduct.type_info.add_view, context=Shop,
             permission='add', renderer='kotti:templates/edit/node.pt')
class ShopProductAddForm(AddFormView):
    item_type = _(u"ShopProduct")
    item_class = ShopProduct

    schema_factory = ShopProductSchema

    def add(self, **appstruct):
        productcategories = appstruct['productcategories']
        producttopics = appstruct['producttopics']
        productmaterials = appstruct['productmaterials']
        productages = appstruct['productages']
        all_tags = set(productcategories + producttopics + productmaterials +
                       productages)
        price = appstruct['price']
        support_days = appstruct['support_days']
        featured = appstruct['featured']
        quantity = appstruct['quantity']
        if quantity > 0:
            if quantity > 5:
                status = _("Available")
            else:
                status = _("Limited")
        else:
            status = _("Not available")

        return self.item_class(
            productcategories=productcategories,
            description=appstruct['description'],
            productmaterials=productmaterials,
            tags=all_tags,
            title=appstruct['title'],
            producttopics=producttopics,
            productages=productages,
            price=price,
            support_days=support_days,
            featured=featured,
            quantity=quantity,
            status=status
        )

    def before(self, form):
        selectize.need()
        return super(ShopProductAddForm, self).before(form)


@view_config(name='edit', context=ShopProduct, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class ShopProductEditForm(EditFormView):
    """ Form to edit existing ShopProduct objects. """

    def schema_factory(self):
        # tmpstore = FileUploadTempStore(self.request)
        # return ShopProductSchema(tmpstore)
        return ShopProductSchema()

    def before(self, form):
        selectize.need()
        return super(ShopProductEditForm, self).before(form)

    def edit(self, **appstruct):
        super(ShopProductEditForm, self).edit(**appstruct)
        product = self.context
        product.productmaterials = appstruct['productmaterials']
        product.productcategories = appstruct['productcategories']
        product.producttopics = appstruct['producttopics']
        product.productages = appstruct['productages']
        all_tags = set(
            appstruct['productcategories'] + appstruct['productmaterials'] +
            appstruct['producttopics'] + appstruct['productages'])
        product.tags = all_tags
        quantity = appstruct['quantity']
        if quantity > 0:
            if quantity > 5:
                status = _("Available")
            else:
                status = _("Limited")
        else:
            status = _("Not available")
        product.quantity = quantity
        product.status = status


@view_config(name='edit_price_offer', context=ShopProduct, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class ShopProductPriceOfferEditForm(EditFormView):
    """ Form to give a special price offer for a product. """

    schema_factory = ShopProductPriceOfferSchema

    def edit(self, **appstruct):
        self.context.price = appstruct['price']
        self.context.price_offer = appstruct['price_offer']
        self.context.expires_offer_date = appstruct['expires_offer_date']


@view_config(name=ShopClient.type_info.add_view, context=Shop,
             permission='add', renderer='kotti:templates/edit/node.pt')
class ShopClientAddForm(AddFormView):
    """ Form to add a client to shop """

    item_type = _(u"ShopClient")
    item_class = ShopClient

    schema_factory = ShopClientSchema

    def add(self, **appstruct):
        name = appstruct['name']
        title = appstruct['title']
        description = appstruct['title']
        nickname = appstruct['name']
        fullname = appstruct['title']
        email = appstruct['email']
        paypal_email = appstruct['paypal_email']
        deliver_address = appstruct['deliver_address']
        status = "new user"
        last_ip_login = self.request.remote_addr
        return self.item_class(
            name=name,
            title=title,
            description=description,
            nickname=nickname,
            fullname=fullname,
            email=email,
            paypal_email=paypal_email,
            deliver_address=deliver_address,
            status=status,
            last_ip_login=last_ip_login
        )


@view_config(name='edit', context=ShopClient,
             permission='edit', renderer='kotti:templates/edit/node.pt')
class ShopClientEditForm(EditFormView):
    """ Form to edit a client info """

    schema_factory = ShopClientSchema

    def edit(self, **appstruct):
        self.context.name = appstruct['name']
        self.context.title = appstruct['title']
        self.context.description = appstruct['title']
        self.context.nickname = appstruct['name']
        self.context.fullname = appstruct['title']
        self.context.email = appstruct['email']
        self.context.paypal_email = appstruct['paypal_email']
        self.context.deliver_address = appstruct['deliver_address']
