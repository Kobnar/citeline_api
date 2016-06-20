from . import resources, views, schemas


def traversal_factory(parent, name):
    sources = resources.SourceCollection(parent, name)
    sources['text'] = resources.TextSourceCollection(sources, 'text')
    sources['text']['books'] = resources.TextSourceCollection(sources['text'], 'books')
    return sources
