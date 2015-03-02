from colander import MappingSchema
from colander import SchemaNode
from colander import Range
from colander import Set
from colander import String
from colander import Int
from deform.widget import CheckboxChoiceWidget
from kotti import get_settings

from kotti_disqus import _
from kotti_settings.util import add_settings


TestSettings = {
    'name': 'test_settings',
    'title': "Testsettings",
    'description': "Some description for my settings",
    'success_message': u"Successfully saved test settings.",
    'settings': [
        {'type': 'String',
         'name': 'testsetting_1',
         'title': 'Test 1',
         'description': 'a test setting',
         'default': '', },
        {'type': 'Integer',
         'name': 'testsetting_2',
         'title': 'Test 2',
         'description': 'again a test setting',
         'default': 23, }]}


class StringSchemaNode(SchemaNode):
    name = 'a_string'
    title = 'hello'
    default = 'hello world'


class RangedIntSchemaNode(SchemaNode):
    name = 'range_int'
    validator = Range(0, 10)
    default = 5
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
