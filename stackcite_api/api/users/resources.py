import logging
import mongoengine
from pyramid import security as sec

from stackcite import data as db

from stackcite_api import resources, auth

from . import schema, views


_LOG = logging.getLogger(__name__)


class ConfirmationResource(
        resources.APIIndexResource, resources.ValidatedResource):

    _VIEW_CLASS = views.ConfirmationViews

    __acl__ = [
        (sec.Allow, sec.Everyone, ('create', 'update'))
    ]

    _SCHEMA = {
        'create': schema.CreateConfirmationToken,
        'update': schema.UpdateConfirmationToken
    }

    def create(self, data):
        """
        Issues a new account confirmation token. Replaces an existing token if
        one already exists in the database.
        """
        data, errors = self.validate('create', data)
        email = data['email']
        user = db.User.objects.get(email=email)
        token = db.ConfirmToken.new(user)
        try:
            token.save()
        except mongoengine.NotUniqueError:
            db.ConfirmToken.objects(_user=user).delete()
            token.save()
        return token

    def update(self, data):
        """
        Confirms a user's registration.
        """
        data, errors = self.validate('update', data)
        key = data['key']
        token = db.ConfirmToken.objects.get(_key=key)
        token.confirm_user()
        return True


class UserDocument(resources.APIDocumentResource):

    def __acl__(self):
        return [
            (sec.Allow, self.id, ('retrieve', 'update', 'delete')),
            (sec.Allow, auth.ADMIN, ('retrieve', 'update', 'delete')),
            sec.DENY_ALL
        ]

    _SCHEMA = {
        'PUT': schema.UpdateUser
    }


class UserCollection(resources.APICollectionResource):

    __acl__ = [
        (sec.Allow, auth.ADMIN, 'retrieve'),
        (sec.Allow, sec.Everyone, 'create'),
        sec.DENY_ALL
    ]

    _COLLECTION = db.User
    _DOCUMENT_RESOURCE = UserDocument

    _OFFSPRING = {
        'confirmation': ConfirmationResource
    }

    _SCHEMA = {
        'POST': schema.CreateUser
    }

    def create(self, data):
        user = super().create(data)
        conf_token = db.ConfirmToken.new(user, save=True)
        _LOG.info('New confirmation token: {}'.format(conf_token.key))
        return user
