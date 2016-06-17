from . import resources, views, schemas

from . import text


def traversal_factory(parent, name):
    sources = resources.SourceCollection(parent, name)
    sources['text'] = text.traversal_factory(sources, 'text')
    return sources
