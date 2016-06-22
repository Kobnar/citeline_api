from . import resources, schemas, views
from . import citations
from . import organizations
from . import people
from . import sources


VERSIONS = ('v0',)
VERSION = VERSIONS[-1]


def traversal_factory(parent, name):
    # Index
    parent[name] = api_idx = resources.APIIndex(parent, name)
    # Collections
    people.traversal_factory(api_idx, 'people')
    organizations.traversal_factory(api_idx, 'organizations')
    sources.traversal_factory(api_idx, 'sources')
    citations.traversal_factory(api_idx, 'citations')
    return parent
