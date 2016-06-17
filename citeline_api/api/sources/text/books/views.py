from pyramid.view import view_defaults, view_config

from citeline_api import api

from . import resources


@view_defaults(context=resources.BookSourceDocument, renderer='json')
class BookSourceDocumentViews(api.views.APIDocumentViews):
    """``../sources/text/{ObjectId}/``"""

    @view_config(request_method='GET')
    def retrieve(self):
        return super().retrieve()

    @view_config(request_method='PUT')
    def update(self):
        return super().update()

    @view_config(request_method='DELETE')
    def delete(self):
        return super().delete()


@view_defaults(context=resources.BookSourceCollection, renderer='json')
class BookSourceCollectionViews(api.views.APICollectionViews):
    """``../sources/text/``"""

    @view_config(request_method='POST')
    def create(self):
        return super().create()

    @view_config(request_method='GET')
    def retrieve(self):
        return super().retrieve()
