import logging
import mongoengine
from contextlib import suppress
from pyramid import security as sec
from stackcite import data as db
from stackcite.api import resources, auth

from . import auth as users_auth
from . import conf as users_conf
from . import schema

_LOG = logging.getLogger(__name__)


class UserDocument(resources.APIDocumentResource):

    def __acl__(self):
        return [
            (sec.Allow, self.id, ('retrieve', 'update', 'delete')),
            (sec.Allow, auth.ADMIN, ('retrieve', 'update', 'delete')),
            sec.DENY_ALL
        ]

    _DOCUMENT_SCHEMA = schema.User
    _SCHEMA = {
        'PUT': schema.UpdateUser
    }

    def update(self, data):
        # TODO: Perform a deep copy instead of mutating existing data
        if data.get('new_password'):
            user = self.retrieve()
            password = data.pop('password')
            if user.check_password(password):
                data['password'] = data.pop('new_password')
        print(data)
        return super().update(data)

    def delete(self):
        # Delete associated CachedReferenceFields
        with suppress(mongoengine.DoesNotExist):
            db.AuthToken.objects(_user__id=self.id).delete()
            db.ConfirmToken.objects(_user__id=self.id).delete()
        return super().delete()


class UserCollection(resources.APICollectionResource):

    __acl__ = [
        (sec.Allow, auth.ADMIN, 'retrieve'),
        (sec.Allow, sec.Everyone, 'create'),
        sec.DENY_ALL
    ]

    _COLLECTION = db.User
    _DOCUMENT_RESOURCE = UserDocument

    _DOCUMENT_SCHEMA = schema.User
    _SCHEMA = {
        'POST': schema.CreateUser
    }

    def create(self, data):
        user = super().create(data)
        conf_token = db.ConfirmToken.new(user, save=True)
        _LOG.info('New confirmation token: {}'.format(conf_token.key))
        return user
