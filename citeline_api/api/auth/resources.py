import mongoengine

from citeline import data as db

from citeline_api import api

from . import schemas


class AuthResource(api.resources.APIIndex):

    _token_schema = schemas.Token
    _auth_schema = schemas.Authenticate

    def log_in(self, auth_data):
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

    def touch(self, token_data):
        schema = self._token_schema(strict=True)
        token_data = schema.load(token_data).data
        key = token_data.get('token')
        token = db.Token.objects.get(_key=key)
        token.save()
        return {
            'touched': str(token.touched)
        }

    def log_out(self, token_data):
        schema = self._token_schema(strict=True)
        token_data = schema.load(token_data).data
        key = token_data.get('token')
        return db.Token.objects(_key=key).delete()
