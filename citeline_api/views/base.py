class BaseView(object):
    """A basic view class.

    NOTE: Class is intended to be sub-classed for different pages.
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
