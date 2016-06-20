def make_citation(data, source, save=False):
    from citeline.data import BookCitation
    citation = BookCitation()
    citation.deserialize(data)
    citation.source = source
    if save:
        citation.save()
    return citation
