from colander import Boolean
from colander import Int
from colander import MappingSchema
from colander import Range
from colander import SchemaNode
from colander import String
from kotti_settings.util import add_settings


class ShopCurrencyNode(SchemaNode):
    name = 'shop_currency'
    title = 'Currency'
    description = 'Price example: 12 USD'
    default = 'USD'


class ShopProductsPerPageNode(SchemaNode):
    name = 'shop_products_per_page'
    title = 'Products per page'
    description = 'How many products will be on a page with products.'
    validator = Range(1, 1000)
    default = 9


class ShopCarouselVisibilityShopViewNode(SchemaNode):
    name = 'shop_carousel_visibility_shop_view'
    title = 'Carousel visibility in shop view'
    description = 'Check it if you want carousel to be visible.'
    default = True


class ShopCarouselVisibilitySearchViewNode(SchemaNode):
    name = 'shop_carousel_visibility_search_view'
    title = 'Carousel visibility in search view'
    description = 'Check it if you want carousel to be visible.'
    default = False


class FeaturedProductsVisibilitySearchViewNode(SchemaNode):
    name = 'featured_products_visibility_search_view'
    title = 'Featured products visibility in search view'
    description = 'Check it to show featured products in search view.'
    default = False


class ProductsLimitedQuantityNode(SchemaNode):
    name = 'shop_products_limited_quantity'
    title = 'Limited quantity'
    description = 'How many items means a product quantity is limited'
    validator = Range(1, 1000)
    default = 5


class ShopSettingsSchema(MappingSchema):
    shop_currency = ShopCurrencyNode(String())
    shop_products_per_page = ShopProductsPerPageNode(Int())
    shop_carousel_visibility_shop_view = ShopCarouselVisibilityShopViewNode(
        Boolean())
    shop_carousel_visibility_search_view = \
        ShopCarouselVisibilitySearchViewNode(Boolean())
    featured_products_visibility_search_view = \
        FeaturedProductsVisibilitySearchViewNode(Boolean())
    shop_products_limited_quantity = ProductsLimitedQuantityNode(Int())


ShopSettings = {
    'name': 'shop_settings',
    'title': "Shop settings",
    'description': "Here you can set your shop.",
    'success_message': u"Successfully saved shop settings.",
    'schema_factory': ShopSettingsSchema
}


def populate():
    add_settings(ShopSettings)
