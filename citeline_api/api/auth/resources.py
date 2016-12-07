import mongoengine

from pyramid import security as sec
from citeline import data as db

from citeline_api import api

from . import schemas, views


class AuthResource(api.resources.APIIndex):

    VIEW_CLASS = views.AuthViews

    __acl__ = [
        (sec.Allow, sec.Authenticated, ('retrieve', 'update', 'delete')),
        (sec.Allow, sec.Everyone, 'create'),
        sec.DENY_ALL
    ]

    _token_schema = schemas.Token
    _auth_schema = schemas.Authenticate

    def create(self, auth_data):
        """
        Creates or updates a :class:`~Token` based on valid user authentication
        credentials.
        """
        schema = self._auth_schema(strict=True)
        auth_data = schema.load(auth_data).data
        email = auth_data.get('email')
        password = auth_data.get('password')
        user = db.User.authenticate(email, password)
        try:
            token = db.Token.objects.get(_user=user)
        except mongoengine.DoesNotExist:
            token = db.Token(_user=user)
        token.save()
        user.touch_login()
        user.save()
        return {
            'user': {
                'id': str(user.id)
            },
            'token': {
                'key': str(token.key),
                'issued': str(token.issued),
                'touched': str(token.touched)
            }
        }

    def retrieve(self, token):
        """
        Confirms the existence of a :class:`~Token`.
        """
        return {
            'user': {
                'id': str(token.user.id)
            },
            'token': {
                'key': str(token.key),
                'issued': str(token.issued),
                'touched': str(token.touched)
            }
        }

    def update(self, token):
        """
        Updates an existing :class:`~Token`.
        """
        token.save()
        return {
            'user': {
                'id': str(token.user.id)
            },
            'token': {
                'key': str(token.key),
                'issued': str(token.issued),
                'touched': str(token.touched)
            }
        }

    def delete(self, token):
        """
        Deletes an existing :class:`~Token`.
        """
        return bool(token.delete())
