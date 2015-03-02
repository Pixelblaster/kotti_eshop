# -*- coding: utf-8 -*-
from datetime import date
from kotti_eshop.resources import Shop
from kotti_eshop.resources import ShopProduct
from kotti_eshop.resources import ShopClient
from kotti_eshop.views import BaseView
from kotti.resources import get_root
from pyramid.view import view_config
from pyramid.view import view_defaults
from webhelpers.paginate import PageURL, Page


@view_config(name='shopping_cart', permission='view',
             renderer='kotti_eshop:templates/shopping-cart.pt')
def shopping_cart(request):
    """ Shopping cart view
    """
    if request.user:
        logged_in_user = request.user.name
    else:
        logged_in_user = ''
    return {'logged_in_user': logged_in_user}


@view_defaults(context=Shop, permission='view')
class ShopViews(BaseView):
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
        return {'products': products,
                'custom_page_title': custom_page_title,
                'today': today}

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
        show_shop_carousel = shop.carousel_visibility_shop_view()
        if featured_products.count() > 0:
            show_featured_products = True
        else:
            show_featured_products = False

        # GET current page. SET to 1 if is None
        get = self.request.GET
        if get.get('page') is not None:
            current_page = get.get('page')
        else:
            current_page = 1

        # SET url format
        url_for_page = PageURL(self.request.resource_url(self.context),
                               {"page": current_page})

        # My collection to be paginated = all activities
        my_collection = products

        # SET page, items, pager
        items_per_page = 1
        my_page = Page(my_collection, page=current_page, url=url_for_page,
                       items_per_page=items_per_page)
        my_page_items = my_page.items

        my_page_pager = my_page.pager(
            format="$link_previous ~2~ $link_next",
            symbol_previous="prev",
            symbol_next="next",
            link_attr={"class": "btn small"},
            curpage_attr={"class": "btn primary small disabled"},
            dotdot_attr={"class": "btn small disabled"})

        return {'products': my_page_items,
                'my_page_pager': my_page_pager,
                'current_page': current_page,
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

        # GET current page. SET to 1 if is None
        get = self.request.GET
        if get.get('page') is not None:
            current_page = get.get('page')
        else:
            current_page = 1

        # Select products by CATEGORY
        if get.get('category') is not None:
            category = get.get('category')
            title_text = category + " in categories"
            products = shop.get_products_by_category(category)
            url_for_page = PageURL(
                self.request.resource_url(shop) +
                '@@search-products',
                {"category": category.encode("utf8"), "page": current_page})
        else:
            # Select products by TOPIC
            if get.get('topic') is not None:
                topic = get.get('topic')
                title_text = topic + " in topics"
                products = shop.get_products_by_topic(topic)
                url_for_page = PageURL(
                    self.request.resource_url(shop) +
                    '@@search-products',
                    {"topic": topic.encode("utf8"), "page": current_page})
            else:
                # Select products by MATERIAL
                if get.get('material') is not None:
                    material = get.get('material')
                    title_text = material + " in materials"
                    products = shop.get_products_by_material(material)
                    url_for_page = PageURL(
                        self.request.resource_url(shop) +
                        '@@search-products',
                        {"material": material.encode("utf8"),
                         "page": current_page})
                else:
                    # Select products by AGE
                    if get.get('age') is not None:
                        age = get.get('age')
                        title_text = age + " in recommended for ages"
                        products = shop.get_products_by_age(age)
                        url_for_page = PageURL(
                            self.request.resource_url(shop) +
                            '@@search-products',
                            {"age": age.encode("utf8"),
                             "page": current_page})
                    else:
                        # No filters.
                        products = shop.get_all_products()
                        title_text = "products in shop"

        custom_page_title = "Search for " + title_text
        show_shop_carousel = shop.carousel_visibility_search_view()
        show_featured_products = False
        featured_products = shop.get_featured_products()

        # My collection to be paginated = all activities
        my_collection = products

        # SET page, items, pager
        items_per_page = 1
        my_page = Page(my_collection, page=current_page, url=url_for_page,
                       items_per_page=items_per_page)
        my_page_items = my_page.items

        my_page_pager = my_page.pager(
            format="$link_previous ~2~ $link_next",
            symbol_previous="prev",
            symbol_next="next",
            link_attr={"class": "btn small"},
            curpage_attr={"class": "btn primary small disabled"},
            dotdot_attr={"class": "btn small disabled"})
        return {'products': my_page_items,
                'my_page_pager': my_page_pager,
                'current_page': current_page,
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


@view_defaults(context=ShopClient, permission='view')
class ShopClientViews(BaseView):
    """ Views for ShopClient """

    @view_config(name='view', permission='view',
                 renderer='kotti_eshop:templates/shopclient-view.pt')
    def shop_product_view(self):
        """ ShopClient View
        """
        today = date.today()
        return {'today': today}
