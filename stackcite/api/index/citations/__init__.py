from .resources import (
    CitationCollection,
    CitationDocument,
    TextCitationCollection,
    TextCitationDocument,
    BookCitationCollection,
    BookCitationDocument
)


def traversal_factory(parent, name):
    citations = CitationCollection(parent, name)
    citations['text'] = TextCitationCollection
    citations['text']['books'] = BookCitationCollection
    return citations
