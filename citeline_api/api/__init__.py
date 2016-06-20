from . import resources, schemas, views
from . import citations
from . import organizations as orgs
from . import people
from . import sources


def traversal_factory(parent, name):
    # Index
    api_idx = resources.APIIndex(parent, name)
    # Collections
    api_idx = people.traversal_factory(api_idx, 'people')
    api_idx = orgs.traversal_factory(api_idx, 'organizations')
    api_idx = sources.traversal_factory(api_idx, 'sources')
    api_idx = citations.traversal_factory(api_idx, 'citations')
    return api_idx
