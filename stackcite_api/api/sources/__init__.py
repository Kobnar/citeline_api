from .resources import (
    SourceCollection,
    SourceDocument,
    TextSourceCollection,
    TextSourceDocument,
    BookSourceCollection,
    BookSourceDocument
)


ENDPOINTS = (
    SourceCollection,
    SourceDocument,
    TextSourceCollection,
    TextSourceDocument,
    BookSourceCollection,
    BookSourceDocument
)


def traversal_factory(parent, name):
    parent[name] = resources.SourceCollection
    parent[name]['text'] = resources.TextSourceCollection
    parent[name]['text']['books'] = resources.BookSourceCollection
    return parent
