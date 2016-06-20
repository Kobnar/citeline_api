from . import resources, views, schemas


def traversal_factory(parent, name):
    txt_srcs = resources.CitationCollection(parent, name)
    txt_srcs['text'] = resources.TextCitationCollection(txt_srcs, 'text')
    txt_srcs['text']['books'] = resources.BookCitationCollection(txt_srcs['text'], 'books')
    return txt_srcs
