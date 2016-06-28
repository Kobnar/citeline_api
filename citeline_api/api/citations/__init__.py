from .resources import (
    CitationCollection,
    CitationDocument,
    TextCitationCollection,
    TextCitationDocument,
    BookCitationCollection,
    BookCitationDocument
)


ENDPOINTS = (
    CitationCollection,
    CitationDocument,
    TextCitationCollection,
    TextCitationDocument,
    BookCitationCollection,
    BookCitationDocument
)


def traversal_factory(parent, name):
    parent[name] = resources.CitationCollection(parent, name)
    parent[name]['text'] = resources.TextCitationCollection(parent[name], 'text')
    parent[name]['text']['books'] = resources.BookCitationCollection(parent[name]['text'], 'books')
    return parent
