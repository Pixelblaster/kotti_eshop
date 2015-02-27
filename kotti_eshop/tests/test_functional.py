# -*- coding: utf-8 -*-
from pytest import mark


# Login must be required for these views:
def test_login_required(webtest, root):
    # Demo [TODO] delete this
    resp = webtest.get('/add_custom_content')
    assert resp.status_code == 302

    # Add a shop to your site
    resp = webtest.get('/add_shop')
    assert resp.status_code == 302


@mark.user('admin')
def test_add(webtest, root):

    resp = webtest.get('/add_custom_content')

    # submit empty form
    form = resp.forms['deform']
    resp = form.submit('save')
    assert 'There was a problem' in resp.body

    # submit valid form
    form = resp.forms['deform']
    form['title'] = 'My Custom Content'
    form['custom_attribute'] = 'My Custom Attribute Value'
    resp = form.submit('save')
    assert resp.status_code == 302
    resp = resp.follow()
    assert 'Item was added.' in resp.body


@mark.user('admin')
def test_edit(webtest, root):

    from kotti_eshop.resources import CustomContent

    root['cc'] = CustomContent(title=u'Content Title')

    resp = webtest.get('/cc/@@edit')
    form = resp.forms['deform']
    assert form['title'].value == u'Content Title'
    assert form['custom_attribute'].value == u''
    form['custom_attribute'] = u'Bazinga'
    resp = form.submit('save').maybe_follow()
    assert u'Your changes have been saved.' in resp.body
    assert u'Bazinga' in resp.body


@mark.user('admin')
def test_add_shop(webtest, root):
    """ Test: Add a shop """
    resp = webtest.get('/add_shop')

    # submit empty form
    form = resp.forms['deform']
    resp = form.submit('save')
    assert 'There was a problem' in resp.body

    # submit valid form
    form = resp.forms['deform']
    form['title'] = 'My Shop'
    resp = form.submit('save')
    assert resp.status_code == 302
    resp = resp.follow()
    assert 'Item was added.' in resp.body


@mark.user('admin')
def test_edit_shop(webtest, root):
    """ Test: Edit a shop """
    from kotti_eshop.resources import Shop

    root['shop'] = Shop(title=u'Shop Title')

    resp = webtest.get('/shop/@@edit')
    form = resp.forms['deform']
    assert form['title'].value == u'Shop Title'
    resp = form.submit('save').maybe_follow()
    assert u'Your changes have been saved.' in resp.body


@mark.user('admin')
def test_add_product(webtest, root):
    """ Test: Add a product to shop """
    from kotti_eshop.resources import Shop
    root['shop'] = Shop(title=u'Shop Title')

    resp = webtest.get('/shop/add_product')

    # submit empty form
    form = resp.forms['deform']
    resp = form.submit('save')
    assert 'There was a problem' in resp.body

    # submit valid form
    form = resp.forms['deform']
    form['title'] = u'A product'
    form['price'] = 20
    form['support_days'] = 365
    form['featured'] = True
    form['status'] = u"Available"

    resp = form.submit('save')
    assert resp.status_code == 302
    resp = resp.follow()
    assert 'Item was added.' in resp.body
