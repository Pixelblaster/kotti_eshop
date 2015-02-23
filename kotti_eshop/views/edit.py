# -*- coding: utf-8 -*-
import colander
from colander import SequenceSchema
from colander import SchemaNode
from colander import String
from deform.widget import SelectWidget
from kotti_eshop import _
from kotti_eshop.fanstatic import selectize
from kotti_eshop.resources import CustomContent
from kotti_eshop.resources import Shop
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


class CustomContentSchema(ContentSchema):
    """ Schema for CustomContent. """

    custom_attribute = colander.SchemaNode(
        colander.String(),
        title=_(u"Custom attribute"))


class ShopSchema(ContentSchema):
    """ Schema for Shop. """


def ShopProductSchema(tmpstore, title_missing=None):
    class ShopProductSchema(ContentSchema):
        productmaterials = ProductMaterials(
            widget=get_selectize_widget(ProductMaterial),
            description=_("Type or select materials"))
        productcategories = ProductCategories(
            widget=get_selectize_widget(ProductCategory),
            description=_("Type or select categories"))
        producttopics = ProductTopics(
            widget=get_selectize_widget(ProductTopic),
            description=_("Type or select topics"))
        productages = ProductAges(
            widget=get_selectize_widget(ProductAge),
            description=_("Type or select ages"))
    return ShopProductSchema()


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
        return self.item_class(
            productcategories=productcategories,
            description=appstruct['description'],
            productmaterials=productmaterials,
            tags=all_tags,
            title=appstruct['title'],
            producttopics=producttopics,
            productages=productages,
        )

    def before(self, form):
        selectize.need()
        return super(ShopProductAddForm, self).before(form)


class ShopProductEditForm(EditFormView):

    def schema_factory(self):
        # tmpstore = FileUploadTempStore(self.request)
        # return ShopProductSchema(tmpstore)
        return ShopProductSchema()

    def before(self, form):
        selectize.need()
        return super(ShopProductEditForm, self).before(form)

    def edit(self, **appstruct):
        super(ShopProductEditForm, self).edit(**appstruct)
        self.context.productmaterials = appstruct['productmaterials']
        self.context.productcategories = appstruct['productcategories']
        self.context.producttopics = appstruct['producttopics']
        self.context.productages = appstruct['productages']
        all_tags = set(
            appstruct['productcategories'] + appstruct['productmaterials'] +
            appstruct['producttopics'] + appstruct['productages'])
        self.context.tags = all_tags


@view_config(name=CustomContent.type_info.add_view, permission='add',
             renderer='kotti:templates/edit/node.pt')
class CustomContentAddForm(AddFormView):
    """ Form to add a new instance of CustomContent. """

    schema_factory = CustomContentSchema
    add = CustomContent
    item_type = _(u"CustomContent")


@view_config(name='edit', context=CustomContent, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class CustomContentEditForm(EditFormView):
    """ Form to edit existing CustomContent objects. """

    schema_factory = CustomContentSchema
