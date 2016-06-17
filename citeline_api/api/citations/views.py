from pyramid.view import view_defaults, view_config

from citeline_api import api

from . import resources


@view_defaults(context=resources.CitationDocument, renderer='json')
class CitationDocumentViews(api.views.APIDocumentViews):
    """``../citations/{ObjectId}/``"""

    @view_config(request_method='GET')
    def retrieve(self):
        return super().retrieve()

    @view_config(request_method='PUT')
    def update(self):
        return super().update()

    @view_config(request_method='DELETE')
    def delete(self):
        return super().delete()


@view_defaults(context=resources.CitationCollection, renderer='json')
class CitationCollectionViews(api.views.APICollectionViews):
    """``../citations/``"""

    @view_config(request_method='POST')
    def create(self):
        return super().create()

    @view_config(request_method='GET')
    def retrieve(self):
        return super().retrieve()
