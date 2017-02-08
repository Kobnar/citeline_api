from . import models


def create_mock_data(count=16, save=False):
    docs = list()
    for n in range(count):
        doc = models.MockDocument(
            name='Document #{}'.format(n),
            number=n,
            fact=bool(n%2))
        if save:
            doc.save()
        docs.append(doc)
    return docs
