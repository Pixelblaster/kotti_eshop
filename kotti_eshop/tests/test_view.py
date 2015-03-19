# -*- coding: utf-8 -*-
from pytest import fixture


# @fixture
# def dummy_shop(root):
#     """ Returns a shop for tests """
#     from kotti_eshop.resources import Shop

#     root['shop'] = shop = Shop(
#         title=u'My Shop',
#         description=u'My very custom content is custom'
#     )

#     return shop


# def test_shop_views(dummy_shop, dummy_request):

#     from kotti_eshop.views.view import ShopViews

#     views = ShopViews(dummy_shop, dummy_request)

#     # test admin view
#     shop_admin_view = views.shop_admin_view()
#     assert 'custom_page_title' in shop_admin_view
#     assert 'products' in shop_admin_view
#     assert 'today' in shop_admin_view

#     # test shop view
#     shop_view = views.shop_view()
#     assert 'products' in shop_view
#     assert 'featured_products' in shop_view
#     assert 'custom_page_title' in shop_view
#     assert 'today' in shop_view
#     assert 'show_featured_products' in shop_view
#     assert 'show_shop_carousel' in shop_view
#     assert shop_view.get('show_shop_carousel') is True
#     if shop_view.get('featured_products').count() > 0:
#         assert shop_view.get('show_featured_products') is True
#     else:
#         assert shop_view.get('show_featured_products') is False

#     # test shop search products view
#     shop_search_products_view = views.shop_search_products_view()
#     assert 'products' in shop_search_products_view
#     assert 'featured_products' in shop_search_products_view
#     assert 'custom_page_title' in shop_search_products_view
#     assert 'today' in shop_search_products_view
#     assert 'show_featured_products' in shop_search_products_view
#     assert 'show_shop_carousel' in shop_search_products_view

#     shop = views.context
#     get = dummy_request.GET
#     # Select products by CATEGORY
#     get['category'] = "A category"
#     if get.get('category') is not None:
#         category = get.get('category')
#         title_text = category + " in categories"
#         products = shop.get_products_by_category(category)
#         assert "in categories" in title_text

#     # Select products by TOPIC
#     get['topic'] = "A topic"
#     if get.get('topic') is not None:
#         topic = get.get('topic')
#         title_text = topic + " in topics"
#         products = shop.get_products_by_topic(topic)
#         assert "in topics" in title_text

#     # Select products by MATERIAL
#     get['material'] = "A material"
#     if get.get('material') is not None:
#         material = get.get('material')
#         title_text = material + " in materials"
#         products = shop.get_products_by_material(material)
#         assert "in materials" in title_text

#     # Select products by AGE
#     get['age'] = "Two years"
#     if get.get('age') is not None:
#         age = get.get('age')
#         title_text = age + " in recommended for ages"
#         products = shop.get_products_by_age(age)
#         assert "ages" in title_text

#     # No filters.
#     products = shop.get_all_products()
#     title_text = "products in shop"
#     assert products == products

#     # test shopping cart view
#     from kotti_eshop.views.view import shopping_cart
#     shopping_cart_view = shopping_cart(dummy_request)
#     assert 'logged_in_user' in shopping_cart_view
