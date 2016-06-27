import mongoengine

from mongoengine import context_managers

from citeline import data as db
from citeline.data.validators import keys


def get_token(request):
    """
    Returns a token key from the request authorization header.
    """

    try:
        auth_type, key = request.authorization
        if auth_type.lower() == 'key' and keys.validate_key(key):
            token = db.Token.objects.get(_key=key)
            return token
    except (ValueError, TypeError):
        return None


def get_user(request):
    """
    Returns a user based on an API key located in the request header.
    """

    try:
        if request.token:
            with context_managers.no_dereference(request.token) as token:
                # TODO: Use a SessionUser object
                return token.user
    except (ValueError, TypeError, mongoengine.DoesNotExist):
        return None


def get_groups(user_id, request):
    """
    Returns a list of groups for the current user if `user_id` matches the `id`
    field of the current request's :class:`citeline.User`.
    """

    return request.user.groups if request.user.id == user_id else []
