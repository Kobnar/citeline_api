from . import auth
from . import conf

from .resources import (
    UserCollection,
    UserDocument
)


def traversal_factory(parent, name):
    users = UserCollection(parent, name)
    users['auth'] = auth.AuthResource
    users['conf'] = conf.ConfirmationResource
    return users
