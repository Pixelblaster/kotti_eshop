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


class ShopSettingsSchema(MappingSchema):
    shop_currency = ShopCurrencyNode(String())
    shop_products_per_page = ShopProductsPerPageNode(Int())


ShopSettings = {
    'name': 'shop_settings',
    'title': "Shop settings",
    'description': "Here you can set your shop.",
    'success_message': u"Successfully saved shop settings.",
    'schema_factory': ShopSettingsSchema
}


def populate():
    add_settings(ShopSettings)
