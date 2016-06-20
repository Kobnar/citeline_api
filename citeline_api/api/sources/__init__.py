from . import resources, views, schemas


def traversal_factory(parent, name):
    parent[name] = resources.SourceCollection(parent, name)
    parent[name]['text'] = resources.TextSourceCollection(parent[name], 'text')
    parent[name]['text']['books'] = resources.BookSourceCollection(parent[name]['text'], 'books')
    return parent
