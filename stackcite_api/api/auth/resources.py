import mongoengine

from pyramid import security as sec
from stackcite import data as db

from stackcite_api import api

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
        return token.serialize()

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
        result = db.Token.objects(_key=token.key).delete()
        return bool(result)
