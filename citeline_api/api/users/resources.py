from citeline import data as db

from citeline_api import api

from . import schemas


class UserDocument(api.resources.APIDocument):

    _update_schema = schemas.UpdateUser


class UserCollection(api.resources.APICollection):

    _collection = db.User
    _document_resource = UserDocument

    _create_schema = schemas.CreateUser
