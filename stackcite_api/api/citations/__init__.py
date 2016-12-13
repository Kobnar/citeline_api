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
    parent[name] = resources.CitationCollection
    parent[name]['text'] = resources.TextCitationCollection
    parent[name]['text']['books'] = resources.BookCitationCollection
    return parent
