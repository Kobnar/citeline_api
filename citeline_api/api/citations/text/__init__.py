from . import resources, views, schemas


def traversal_factory(parent, name):
    sources = resources.TextCitationCollection(parent, name)
    return sources
