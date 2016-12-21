import logging
from pyramid import security as sec

from stackcite import data as db

from stackcite_api import resources, auth

from . import schema


_LOG = logging.getLogger(__name__)


class ConfirmationResource(
        resources.APIIndexResource, resources.ValidatedResource):

    _SCHEMA = {
        'create': schema.CreateConfirmationToken,
        'update': schema.ConfirmConfirmationToken
    }

    def create(self, data):
        """
        Creates a new confirmation token and dispatches an email request to
        the end-user.
        """
        data, errors = self.validate('create', data)
        user_id = data['user']
        user = db.User.objects.get(id=user_id)
        token = db.ConfirmToken.new(user, save=True)
        # Dispatch new email

        # If user is already confirmed, return 409 CONFLICT

    def update(self):
        """
        Confirms a user's registration.
        """
        # Accept confirmation key
        # Confirm user account


class UserDocument(resources.APIDocumentResource):

    def __acl__(self):
        return [
            (sec.Allow, self.id, ('retrieve', 'update', 'delete')),
            (sec.Allow, auth.ADMIN, ('retrieve', 'update', 'delete')),
            sec.DENY_ALL
        ]

    _OFFSPRING = {
        'confirmation': ConfirmationResource
    }

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

    _SCHEMA = {
        'POST': schema.CreateUser
    }

    def create(self, data):
        user = super().create(data)
        conf_token = db.ConfirmToken.new(user, save=True)
        _LOG.info('New confirmation token: {}'.format(conf_token.key))
        return user
