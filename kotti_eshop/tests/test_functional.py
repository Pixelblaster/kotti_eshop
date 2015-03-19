# -*- coding: utf-8 -*-
from pytest import mark


# Login must be required for these views:
def test_login_required(webtest, root):
    # Add a shop to your site
    # resp = webtest.get('/add_shop')
    # assert resp.status_code == 302
    # [TODO] Add here all views that requires login
    pass


@mark.user('admin')
def test_add(webtest, root):

    # resp = webtest.get('/add_custom_content')

    # submit empty form
    # form = resp.forms['deform']
    # resp = form.submit('save')
    # assert 'There was a problem' in resp.body

    # submit valid form
    # form = resp.forms['deform']
    # form['title'] = 'My Custom Content'
    # form['custom_attribute'] = 'My Custom Attribute Value'
    # resp = form.submit('save')
    # assert resp.status_code == 302
    # resp = resp.follow()
    # assert 'Item was added.' in resp.body
    # [TODO] Put Add views here
    pass


@mark.user('admin')
def test_add_shop(webtest, root):
    # """ Test: Add a shop """
    # resp = webtest.get('/add_shop')

    # # submit empty form
    # form = resp.forms['deform']
    # resp = form.submit('save')
    # assert 'There was a problem' in resp.body

    # # submit valid form
    # form = resp.forms['deform']
    # form['title'] = 'My Shop'
    # resp = form.submit('save')
    # assert resp.status_code == 302
    # resp = resp.follow()
    # assert 'Item was added.' in resp.body
    pass


# @mark.user('admin')
# def test_edit_shop(webtest, root):
#     """ Test: Edit a shop """
#     from kotti_eshop.resources import Shop

#     root['shop'] = Shop(title=u'Shop Title')

#     resp = webtest.get('/shop/@@edit')
#     form = resp.forms['deform']
#     assert form['title'].value == u'Shop Title'
#     resp = form.submit('save').maybe_follow()
#     assert u'Your changes have been saved.' in resp.body


# @mark.user('admin')
# def test_add_product(webtest, root):
#     """ Test: Add a product to shop """
#     from kotti_eshop.resources import Shop
#     root['shop'] = Shop(title=u'Shop Title')

#     resp = webtest.get('/shop/add_product')

#     # submit empty form
#     form = resp.forms['deform']
#     resp = form.submit('save')
#     assert 'There was a problem' in resp.body

#     # submit valid form
#     form = resp.forms['deform']
#     form['title'] = u'A product'
#     form['price'] = 20
#     form['support_days'] = 365
#     form['featured'] = True
#     form['status'] = u"Available"

#     resp = form.submit('save')
#     assert resp.status_code == 302
#     resp = resp.follow()
#     assert 'Item was added.' in resp.body


# @mark.user('admin')
# def test_edit_product(webtest, root):
#     """ Test: Edit a product """
#     from kotti_eshop.resources import Shop
#     from kotti_eshop.resources import ShopProduct

#     root['shop'] = Shop(title=u'Shop Title')
#     root['shop']['product'] = ShopProduct(
#         title=u'Product',
#         description=u'product description',
#         price=20,
#         support_days=365,
#         featured=True,
#         status=u'Not Available'
#         )
#     resp = webtest.get('/shop/product/@@edit')
#     form = resp.forms['deform']
#     assert form['title'].value == u'Product'
#     resp = form.submit('save').maybe_follow()
#     assert u'Your changes have been saved.' in resp.body


# @mark.user('admin')
# def test_edit_product_price_offer(webtest, root):
#     """ Test: Edit a product price offer """
#     from kotti_eshop.resources import Shop
#     from kotti_eshop.resources import ShopProduct

#     root['shop'] = Shop(title=u'Shop Title')
#     root['shop']['product'] = ShopProduct(
#         title=u'Product',
#         description=u'product description',
#         price=20,
#         support_days=365,
#         featured=True,
#         status=u'Not Available'
#         )

#     # edit price offer
#     product = root['shop']['product']
#     product.price = 20
#     product.price_offer = 10
#     import datetime
#     expires_date = datetime.date.today() + datetime.timedelta(days=10)
#     product.expires_offer_date = expires_date

#     # test changes
#     resp = webtest.get('/shop/product/@@edit_price_offer')
#     form = resp.forms['deform']
#     assert form['price'].value == '20.0'
#     assert form['price_offer'].value == '10.0'
#     assert product.expires_offer_date == expires_date
#     resp = form.submit('save').maybe_follow()
#     assert u'Your changes have been saved.' in resp.body


# @mark.user('admin')
# def test_add_client(webtest, root):
#     """ Test: Add a client to shop """
#     from kotti_eshop.resources import Shop
#     root['shop'] = Shop(title=u'Shop Title')

#     resp = webtest.get('/shop/add_client')

#     # submit empty form
#     form = resp.forms['deform']
#     resp = form.submit('save')
#     assert 'There was a problem' in resp.body

#     # submit valid form
#     form = resp.forms['deform']
#     form['name'] = u'GhitaB'
#     form['title'] = u'Ghita Bizau'
#     form['email'] = u'ghita_bizau@yahoo.com'
#     form['paypal_email'] = u'ghita_bizau@yahoo.com'  # Please donate. :)
#     form['deliver_address'] = u'My Address Here Romania'

#     resp = form.submit('save')
#     assert resp.status_code == 302
#     resp = resp.follow()
#     assert 'Item was added.' in resp.body


# @mark.user('admin')
# def test_edit_client(webtest, root):
#     """ Test: Edit a client details """
#     from kotti_eshop.resources import Shop
#     from kotti_eshop.resources import ShopClient

#     root['shop'] = Shop(title=u'Shop Title')
#     root['shop']['GhitaB'] = ShopClient(
#         name=u'GhitaB',
#         title=u'Ghita Bizau',
#         email=u'ghita_bizau@yahoo.com',
#         paypal_email=u'ghita_bizau@yahoo.com',
#         deliver_address=u'My Address Here Romania'
#         )

#     # test changes
#     resp = webtest.get('/shop/GhitaB/@@edit')
#     form = resp.forms['deform']
#     assert form['name'].value == u'GhitaB'
#     resp = form.submit('save').maybe_follow()
#     assert u'Your changes have been saved.' in resp.body
