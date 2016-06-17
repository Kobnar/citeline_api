from . import resources, views, schemas

from . import books


def traversal_factory(parent, name):
    text = resources.TextSourceCollection(parent, name)
    text['books'] = books.traversal_factory(text, 'books')
    return text
