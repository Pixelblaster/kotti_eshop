# -*- coding: utf-8 -*-


class BaseView(object):
    """ Base class for views """

    def __init__(self, context, request):
        """ Constructor

        :param context: Context of the view
        :type context: :class:`kotti.resources.Content`

        :param request: Current request
        :type request: :class:`kotti.request.Request`
        """

        super(BaseView, self).__init__()

        self.context = context
        self.request = request
