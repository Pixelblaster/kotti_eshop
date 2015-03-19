from colander import MappingSchema
from colander import SchemaNode
from colander import String
from kotti_settings.util import add_settings


class ShopCurrencyNode(SchemaNode):
    name = 'shop_currency'
    title = 'Currency'
    description = 'Price example: 12 USD'
    default = 'USD'


class ShopSettingsSchema(MappingSchema):
    shop_currency = ShopCurrencyNode(String())


ShopSettings = {
    'name': 'shop_settings',
    'title': "Shop settings",
    'description': "Here you can set your shop.",
    'success_message': u"Successfully saved shop settings.",
    'schema_factory': ShopSettingsSchema
}


def populate():
    add_settings(ShopSettings)
