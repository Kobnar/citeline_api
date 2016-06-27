import mongoengine

from mongoengine import context_managers

from citeline import data as db


def get_user(request):
    """
    Returns a user based on an API key located in the request header.
    """

    try:
        auth_type, key = request.authorization
        if auth_type.lower() == 'key':
            with context_managers.no_dereference(db.Token) as Token:
                token = Token.objects.get(_key=key)
                return token.user
    except (ValueError, TypeError, mongoengine.DoesNotExist):
        return None


def get_groups(user_id, request):
    """
    Returns a list of groups for the current user if `user_id` matches the `id`
    field of the current request's :class:`citeline.User`.
    """

    user = request.user
    return user.groups if user.id == user_id else []
