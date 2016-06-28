import mongoengine

from pyramid import security as sec
from citeline import data as db

from citeline_api import api

from . import schemas


class AuthResource(api.resources.APIIndex):

    __acl__ = [
        (sec.Allow, sec.Everyone, 'create'),
        # TODO: Only allow owners of a key to RUD that key!
        (sec.Allow, sec.Authenticated, ('retrieve', 'update', 'delete'))
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
            'user': str(token.user.id),
            'token': str(token.key)
        }

    def retrieve(self, token):
        """
        Confirms the existence of a :class:`~Token`.
        """
        return token.serialize()

    def update(self, token):
        """
        Updates an existing :class:`~Token`.
        """
        token.save()
        return token.serialize()

    def delete(self, token):
        """
        Deletes an existing :class:`~Token`.
        """
        return bool(token.delete())
