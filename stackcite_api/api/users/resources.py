from pyramid import security as sec

from stackcite import data as db

from stackcite_api import resources, auth

from . import schema


class UserDocument(resources.APIDocument):

    def __acl__(self):
        return [
            (sec.Allow, self.id, ('retrieve', 'update', 'delete')),
            (sec.Allow, auth.ADMIN, ('retrieve', 'update', 'delete')),
            sec.DENY_ALL
        ]

    _SCHEMA = {
        'PUT': schema.UpdateUser
    }


class UserCollection(resources.APICollection):

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
