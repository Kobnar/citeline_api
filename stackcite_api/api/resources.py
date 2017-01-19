from pyramid import security as sec
from stackcite_api import api, resources

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

    _OFFSPRING = {
        'citations': api.citations.CitationCollection,
        'organizations': api.organizations.OrganizationCollection,
        'people': api.people.PersonCollection,
        'sources': api.sources.SourceCollection,
        'users': api.users.UserCollection
    }
