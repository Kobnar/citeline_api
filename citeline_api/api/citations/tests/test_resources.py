def make_citation(data, source, save=False):
    from citeline.data import Citation
    citation = Citation()
    citation.deserialize(data)
    citation.source = source
    if save:
        citation.save()
    return citation
