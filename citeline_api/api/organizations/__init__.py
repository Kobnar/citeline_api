from . import resources, views, schemas


def traversal_factory(parent, name):
    parent[name] = resources.OrganizationCollection(parent, name)
    parent[name]['publishers'] = resources.PublisherCollection(parent[name], 'publishers')
    return parent
