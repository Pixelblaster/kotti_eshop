# -*- coding: utf-8 -*-
from datetime import date
from kotti_eshop import _
from kotti_eshop.resources import CustomContent
from kotti_eshop.resources import Shop
from kotti_eshop.resources import ShopProduct
from kotti_eshop.fanstatic import css_and_js
from kotti_eshop.views import BaseView
from pyramid.view import view_config
from pyramid.view import view_defaults


@view_defaults(context=Shop, permission='view')
class ShopView(BaseView):
    """ Views for ShopProduct """

    @view_config(name='admin', permission='view',
                 renderer='kotti_eshop:templates/shop-admin-view.pt')
    def shop_admin_view(self):
        """ Shop administration panel
        """
        shop = self.context
        today = date.today()
        custom_page_title = "Administration Panel"
        products = shop.get_all_products()
        featured_products = shop.get_featured_products()
        show_shop_carousel = True
        return {'products': products,
                'featured_products': featured_products,
                'custom_page_title': custom_page_title,
                'today': today,
                'show_shop_carousel': show_shop_carousel}

    @view_config(name='view', permission='view',
                 renderer='kotti_eshop:templates/shop-view.pt')
    def shop_view(self):
        """ Shop View
        """
        shop = self.context
        products = shop.get_all_products()
        today = date.today()
        custom_page_title = "Products"
        featured_products = shop.get_featured_products()
        show_shop_carousel = True
        if featured_products.count() > 0:
            show_featured_products = True
        else:
            show_featured_products = False
        return {'products': products,
                'featured_products': featured_products,
                'custom_page_title': custom_page_title,
                'today': today,
                'show_shop_carousel': show_shop_carousel,
                'show_featured_products': show_featured_products}

    @view_config(name='search-products', permission='view',
                 renderer='kotti_eshop:templates/shop-view.pt')
    def shop_search_products_view(self):
        """ Shop Search Products View
        """
        today = date.today()
        get = self.request.GET
        shop = self.context

        products = []
        title_text = ""
        # Select products by CATEGORY
        if get.get('category') is not None:
            category = get.get('category')
            title_text = category + " in categories"
            products = shop.get_products_by_category(category)

        else:
            # Select products by TOPIC
            if get.get('topic') is not None:
                topic = get.get('topic')
                title_text = topic + " in topics"
                products = shop.get_products_by_topic(topic)

            else:
                # Select products by MATERIAL
                if get.get('material') is not None:
                    material = get.get('material')
                    title_text = material + " in materials"
                    products = shop.get_products_by_material(material)

                else:
                    # Select products by AGE
                    if get.get('age') is not None:
                        age = get.get('age')
                        title_text = age + " in recommended for ages"
                        products = shop.get_products_by_age(age)

                    else:
                        # No filters.
                        products = shop.get_all_products()
                        title_text = "products in shop"

        custom_page_title = "Search for " + title_text
        show_shop_carousel = False
        show_featured_products = False
        featured_products = shop.get_featured_products()
        return {'products': products,
                'featured_products': featured_products,
                'custom_page_title': custom_page_title,
                'today': today,
                'show_shop_carousel': show_shop_carousel,
                'show_featured_products': show_featured_products}


@view_defaults(context=ShopProduct, permission='view')
class ShopProductViews(BaseView):
    """ Views for ShopProduct """

    @view_config(name='view', permission='view',
                 renderer='kotti_eshop:templates/shopproduct-view.pt')
    def shop_product_view(self):
        """ ShopProduct View
        """
        today = date.today()
        return {'today': today}


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
