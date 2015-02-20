# -*- coding: utf-8 -*-
import colander
from kotti.views.edit import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.view import view_config

from kotti_eshop import _
from kotti_eshop.resources import CustomContent
from kotti_eshop.resources import Shop


class CustomContentSchema(ContentSchema):
    """ Schema for CustomContent. """

    custom_attribute = colander.SchemaNode(
        colander.String(),
        title=_(u"Custom attribute"))


class ShopSchema(ContentSchema):
    """ Schema for Shop. """


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
