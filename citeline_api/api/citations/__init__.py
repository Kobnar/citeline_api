from . import resources, views, schemas


def traversal_factory(parent, name):
    sources = resources.CitationCollection(parent, name)
    return sources
