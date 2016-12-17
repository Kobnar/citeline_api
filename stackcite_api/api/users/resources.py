from pyramid import security as sec

from stackcite import data as db

from stackcite_api import api, auth

from . import schema


class UserDocument(api.resources.APIDocument):

    def __acl__(self):
        return [
            (sec.Allow, self.id, ('retrieve', 'update', 'delete')),
            (sec.Allow, auth.ADMIN, ('retrieve', 'update', 'delete')),
            sec.DENY_ALL
        ]

    _schema = {
        'PUT': schema.UpdateUser
    }


class UserCollection(api.resources.APICollection):

    __acl__ = [
        (sec.Allow, auth.ADMIN, 'retrieve'),
        (sec.Allow, sec.Everyone, 'create'),
        sec.DENY_ALL
    ]

    _schema = {
        'POST': schema.CreateUser
    }

    _collection = db.User
    _document_resource = UserDocument
