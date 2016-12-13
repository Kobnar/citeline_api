import mongoengine
import marshmallow
import stackcite

from pyramid.view import view_defaults, view_config

from stackcite_api import api, views
from stackcite_api.api import exceptions

from . import resources


@view_defaults(renderer='json')
class AuthViews(views.BaseView):
    """``../auth/``"""

    METHODS = (
        ('POST', 'create'),
        ('GET', 'retrieve'),
        ('PUT', 'update'),
        ('DELETE', 'delete')
    )

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

        except (mongoengine.DoesNotExist, stackcite.AuthenticationError):
            msg = 'Authentication failed'
            raise exceptions.APIBadRequest(detail=msg)

    def retrieve(self):
        token = self.request.token
        return self.context.retrieve(token)

    def update(self):
        token = self.request.token
        return self.context.update(token)

    def delete(self):
        token = self.request.token
        result = self.context.delete(token)
        if result:
            raise exceptions.APINoContent()
        else:
            raise exceptions.APINotFound()
