from kotti_settings.util import get_setting
from kotti_eshop.populate import populate


def test_kotti_eshop_settings(webtest, root):
    """ Test kotti_settings for kotti_eshop
    """
    populate()
    shop_currency = get_setting('shop_currency')
    shop_currency = "RON"
    assert shop_currency is not None
