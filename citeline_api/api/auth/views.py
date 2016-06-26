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

    @view_config(request_method='POST')
    def log_in(self):
        try:
            auth_data = self.request.json_body
            return self.context.log_in(auth_data)

        except ValueError:
            msg = 'Failed to decode JSON body'
            raise api.exceptions.APIBadRequest(detail=msg)

        except marshmallow.ValidationError as err:
            msg = err.messages
            raise exceptions.APIBadRequest(detail=msg)

        except (mongoengine.DoesNotExist, citeline.AuthenticationError):
            msg = 'Authentication failed'
            raise exceptions.APIBadRequest(detail=msg)

    @view_config(request_method='PUT')
    def touch(self):
        try:
            token_data = self.request.json_body
            return self.context.touch(token_data)

        except ValueError:
            msg = 'Failed to decode JSON body'
            raise api.exceptions.APIBadRequest(detail=msg)

        except marshmallow.ValidationError as err:
            msg = err.messages
            raise exceptions.APIBadRequest(detail=msg)

        except mongoengine.DoesNotExist:
            raise exceptions.APINotFound()

    @view_config(request_method='DELETE')
    def log_out(self):
        try:
            token_data = self.request.json_body
            result = self.context.log_out(token_data)

        except ValueError:
            msg = 'Failed to decode JSON body'
            raise api.exceptions.APIBadRequest(detail=msg)

        except marshmallow.ValidationError as err:
            msg = err.messages
            raise exceptions.APIBadRequest(detail=msg)

        if result:
            raise exceptions.APINoContent()
        else:
            raise exceptions.APINotFound()
