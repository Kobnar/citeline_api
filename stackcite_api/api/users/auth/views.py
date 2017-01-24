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
            raise exceptions.APIDecodingError()

        except marshmallow.ValidationError as err:
            errors = err.messages
            raise exceptions.APIValidationError(detail=errors)

        except (mongoengine.DoesNotExist, stackcite.AuthenticationError):
            raise exceptions.APIAuthenticationFailed()

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
