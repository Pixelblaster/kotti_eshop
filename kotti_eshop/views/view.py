# -*- coding: utf-8 -*-
from kotti_eshop import _
from kotti_eshop.resources import CustomContent
from kotti_eshop.resources import ShopProduct
from kotti_eshop.fanstatic import css_and_js
from kotti_eshop.views import BaseView
from pyramid.view import view_config
from pyramid.view import view_defaults


@view_config(context=ShopProduct, name='view', permission='view',
             renderer='kotti_eshop:templates/shopproduct-view.pt')
class ShopProductView(BaseView):
    """ Shop product view """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return {}


@view_defaults(context=CustomContent, permission='view')
class CustomContentViews(BaseView):
    """ Views for :class:`kotti_eshop.resources.CustomContent` """

    @view_config(name='view', permission='view',
                 renderer='kotti_eshop:templates/custom-content-default.pt')
    def default_view(self):
        """ Default view for :class:`kotti_eshop.resources.CustomContent`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        return {
            'foo': _(u'bar'),
        }

    @view_config(
        name='alternative-view', permission='view',
        renderer='kotti_eshop:templates/custom-content-alternative.pt')
    def alternative_view(self):
        """ Alternative view for :class:`kotti_eshop.resources.CustomContent`.
        This view requires the JS / CSS resources defined in
        :mod:`kotti_eshop.fanstatic`.

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        css_and_js.need()

        return {
            'foo': _(u'bar'),
        }
