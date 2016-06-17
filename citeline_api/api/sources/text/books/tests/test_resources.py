def make_book(data, authors, editors=None, save=False):
    from citeline.data import BookSource
    source = BookSource()
    source.deserialize(data)
    source.authors = authors
    source.editors = editors
    if save:
        source.save()
    return source
