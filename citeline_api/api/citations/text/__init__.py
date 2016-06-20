from . import resources, views, schemas

from . import books


def traversal_factory(parent, name):
    bk_sources = resources.TextCitationCollection(parent, name)
    bk_sources['books'] = books.traversal_factory(bk_sources, 'books')
    return bk_sources
