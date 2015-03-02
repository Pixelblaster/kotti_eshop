from colander import MappingSchema
from colander import SchemaNode
from colander import Range
from colander import String
from colander import Int

from kotti_settings.util import add_settings


class ShopCurrency(SchemaNode):
    name = 'Currency'
    title = 'Currency'
    default = 'USD'


class ShopProductsPerPage(SchemaNode):
    name = 'Products per page'
    validator = Range(1, 1000)
    default = 9
    title = 'Ranged Int'


class TestSchema(MappingSchema):
    string = StringSchemaNode(String())
    ranged_int = RangedIntSchemaNode(Int())

TestSettings = {
    'name': 'test_settings',
    'title': "Testsettings",
    'description': "Some description for my settings",
    'success_message': u"Successfully saved test settings.",
    'schema_factory': TestSchema
}


def populate():
    add_settings(TestSettings)
