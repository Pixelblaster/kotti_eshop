from kotti.util import LinkBase
from kotti.util import Link
from kotti.resources import get_root


class RouteLink(LinkBase):
    def __init__(self, route_name, title, **kw):
        self.route_name = route_name
        self.title = title
        self.kw = kw

    def visible(self, context, request):
        try:
            request.route_url(self.route_name, **self.kw)
            return True
        except KeyError:
            return False

    def url(self, context, request):
        return request.route_url(self.route_name, **self.kw)


class RootLink(Link):

    def selected(self, context, request):
        root = get_root()
        return super(RootLink, self).selected(root, request)

    def permitted(self, context, request):
        root = get_root()
        return super(RootLink, self).permitted(root, request)

    def visible(self, context, request):
        root = get_root()
        return super(RootLink, self).visible(root, request)

    def url(self, context, request):
        root = get_root()
        return super(RootLink, self).url(root, request)
