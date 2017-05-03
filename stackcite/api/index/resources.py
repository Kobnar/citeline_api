from pyramid import security as sec
from stackcite.api import index, resources

from . import views


class APIIndex(resources.APIIndexResource):
    """
    The root API index resource.
    """

    _VIEW_CLASS = views.APIIndexViews

    __acl__ = [
        (sec.Allow, sec.Everyone, 'retrieve'),
        sec.DENY_ALL
    ]
