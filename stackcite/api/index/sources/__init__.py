from .resources import (
    SourceCollection,
    SourceDocument,
    TextSourceCollection,
    TextSourceDocument,
    BookSourceCollection,
    BookSourceDocument
)


def traversal_factory(parent, name):
    sources = SourceCollection(parent, name)
    sources['text'] = TextSourceCollection
    sources['text']['books'] = BookSourceCollection
    return sources
