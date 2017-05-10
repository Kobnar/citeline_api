import marshmallow
import mongoengine
from mongoengine import context_managers
import stackcite
from pyramid.view import view_defaults
from stackcite import data as db
from stackcite.api import views, exceptions


_FILTER = (
    'key',
    'user.id',
    'user.groups',
    'issued',
    'touched'
)


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
            auth_data = self.context.load(auth_data, method='CREATE').data
            auth_token = self.context.create(auth_data)
            with context_managers.no_dereference(db.AuthToken):
                auth_token = self.context.dump(auth_token).data
            return auth_token

        except ValueError:
            raise exceptions.APIDecodingError()

        except marshmallow.ValidationError as err:
            errors = err.messages
            raise exceptions.APIValidationError(detail=errors)

        except (mongoengine.DoesNotExist, stackcite.data.AuthenticationError):
            raise exceptions.APIAuthenticationFailed()

    def retrieve(self):
        token = self.request.token
        auth_token = self.context.retrieve(token)
        auth_token = self.context.dump(auth_token).data
        return auth_token

    def update(self):
        token = self.request.token
        auth_token = self.context.update(token)
        auth_token = self.context.dump(auth_token).data
        return auth_token

    def delete(self):
        token = self.request.token
        self.context.delete(token)
        raise exceptions.APINoContent()
