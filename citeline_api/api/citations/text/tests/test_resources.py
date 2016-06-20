def make_citation(data, source, save=False):
    from citeline.data import TextCitation
    citation = TextCitation()
    citation.deserialize(data)
    citation.source = source
    if save:
        citation.save()
    return citation
