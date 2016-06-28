import mongoengine
import marshmallow
import citeline

from pyramid.view import view_defaults, view_config

from citeline_api import api, views
from citeline_api.api import exceptions

from . import resources


@view_defaults(context=resources.AuthResource, renderer='json')
class AuthViews(views.BaseView):
    """``../auth/``"""

    @view_config(request_method='POST', permission='create')
    def create(self):
        try:
            auth_data = self.request.json_body
            return self.context.create(auth_data)

        except ValueError:
            msg = 'Failed to decode JSON body'
            raise api.exceptions.APIBadRequest(detail=msg)

        except marshmallow.ValidationError as err:
            msg = err.messages
            raise exceptions.APIBadRequest(detail=msg)

        except (mongoengine.DoesNotExist, citeline.AuthenticationError):
            msg = 'Authentication failed'
            raise exceptions.APIBadRequest(detail=msg)

    @view_config(request_method='GET', permission='retrieve')
    def retrieve(self):
        token = self.request.token
        return self.context.retrieve(token)

    @view_config(request_method='PUT', permission='update')
    def update(self):
        token = self.request.token
        return self.context.update(token)

    @view_config(request_method='DELETE', permission='delete')
    def delete(self):
        token = self.request.token
        result = self.context.delete(token)
        if result:
            raise exceptions.APINoContent()
        else:
            raise exceptions.APINotFound()
