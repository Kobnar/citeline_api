import marshmallow
import mongoengine
import stackcite
from pyramid.view import view_defaults
from stackcite_api import views, exceptions


@view_defaults(renderer='json')
class AuthViews(views.BaseView):
    """``../auth/``"""

    METHODS = {
        'POST': 'create',
        'GET': 'retrieve',
        'PUT': 'update',
        'DELETE': 'delete'
    }

    def create(self):
        try:
            auth_data = self.request.json_body
            self.request.response.status_code = 201
            auth_token = self.context.create(auth_data)
            return auth_token.serialize()

        except ValueError:
            msg = 'Failed to decode JSON body'
            raise exceptions.APIBadRequest(detail=msg)

        except marshmallow.ValidationError as err:
            msg = err.messages
            raise exceptions.APIBadRequest(detail=msg)

        except (mongoengine.DoesNotExist, stackcite.AuthenticationError):
            msg = 'Authentication failed'
            raise exceptions.APIBadRequest(detail=msg)

    def retrieve(self):
        token = self.request.token
        auth_token = self.context.retrieve(token)
        return auth_token.serialize()

    def update(self):
        token = self.request.token
        auth_token = self.context.update(token)
        return auth_token.serialize()

    def delete(self):
        token = self.request.token
        self.context.delete(token)
        raise exceptions.APINoContent()
