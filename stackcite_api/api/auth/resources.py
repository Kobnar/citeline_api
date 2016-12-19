from pyramid import security as sec
from stackcite import data as db

from stackcite_api import resources

from . import schema, views


class AuthResource(resources.APIIndexResource, resources.ValidatedResource):

    _VIEW_CLASS = views.AuthViews

    __acl__ = [
        (sec.Allow, sec.Authenticated, ('retrieve', 'update', 'delete')),
        (sec.Allow, sec.Everyone, 'create'),
        sec.DENY_ALL
    ]

    _SCHEMA = {
        'CREATE': schema.Authenticate
    }

    def create(self, data):
        """
        Creates or updates a :class:`~Token` based on valid user authentication
        credentials.
        """
        data, errors = self.validate('CREATE', data)
        email = data['email']
        password = data['password']
        user = db.User.authenticate(email, password)
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
        if token:
            token.delete()
            return True
        else:
            return False
