from stackcite.api.index.users import auth

from . import citations
from . import organizations
from . import people
from . import sources
from . import users
from .resources import APIIndex

VERSIONS = ('v0',)
VERSION = VERSIONS[-1]


def traversal_factory(parent):
    api = APIIndex(parent, VERSION)
    api['people'] = people.traversal_factory
    api['organizations'] = organizations.traversal_factory
    api['sources'] = sources.traversal_factory
    api['citations'] = citations.traversal_factory
    api['users'] = users.traversal_factory
    return api
