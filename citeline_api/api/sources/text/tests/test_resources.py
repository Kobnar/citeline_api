def make_text(data, authors, editors=None, save=False):
    from citeline.data import TextSource
    source = TextSource()
    source.deserialize(data)
    source.authors = authors
    source.editors = editors
    if save:
        source.save()
    return source
