# -*- coding: utf-8 -*-

from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

from js.jquery import jquery


library = Library("kotti_eshop", "static")

css = Resource(
    library,
    "styles.css",
    minified="styles.min.css")
js = Resource(
    library,
    "scripts.js",
    minified="scripts.min.js")

css_and_js = Group([css, js])

selectize_default_css = Resource(library, "selectize.default.css")
selectize_bootstrap_css = Resource(library, "selectize.bootstrap3.css")
selectize_js = Resource(library, "selectize.js", depends=[jquery])
selectize_extra_js = Resource(library, "integrate-selectize.js",
                              depends=[selectize_js])

selectize = Group([selectize_js, selectize_extra_js, selectize_bootstrap_css])
