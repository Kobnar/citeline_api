from . import resources, views, schemas

from . import text


def traversal_factory(parent, name):
    txt_sources = resources.CitationCollection(parent, name)
    txt_sources['text'] = text.traversal_factory(txt_sources, 'text')
    return txt_sources
