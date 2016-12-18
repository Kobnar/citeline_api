from pyramid import security as sec

from stackcite_api import resources

from . import views


class APIIndex(resources.IndexResource):
    """
    The root index resource.
    """

    VIEW_CLASS = views.APIIndexViews

    __acl__ = [
        (sec.Allow, sec.Everyone, 'retrieve'),
        sec.DENY_ALL
    ]
