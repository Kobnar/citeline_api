from . import resources, schemas, views
from . import citations
from . import organizations as orgs
from . import people
from . import sources


def traversal_factory(parent, name):
    api_idx = resources.APIIndex(parent, name)
    api_idx['people'] = people.traversal_factory(api_idx, 'people')
    api_idx['organizations'] = orgs.traversal_factory(api_idx, 'organizations')
    api_idx['sources'] = sources.traversal_factory(api_idx, 'sources')
    api_idx['citations'] = citations.traversal_factory(api_idx, 'citations')
    return api_idx
