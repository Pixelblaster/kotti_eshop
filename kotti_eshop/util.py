from kotti.util import LinkBase


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
