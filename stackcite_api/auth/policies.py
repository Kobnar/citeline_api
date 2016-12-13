from zope.interface import implementer

from pyramid.interfaces import IAuthenticationPolicy
from pyramid.authentication import CallbackAuthenticationPolicy

from . import utils


@implementer(IAuthenticationPolicy)
class TokenAuthenticationPolicy(CallbackAuthenticationPolicy):
    """
    A custom REST authentication policy that evaluates an `api_key` provided in
    the request header against those saved in the database.
    """

    def __init__(self, callback=None, debug=False):
        self.callback = callback or utils.get_groups
        self.debug = debug

    def unauthenticated_userid(self, request):
        """
        Resolves a :class:`stackcite.Token` key to retrieve the
        :class:`bson.ObjectId` of a :class:`stackcite.User`. If the token
        does not exist, method returns `None`.
        """
        return request.user.id if request.user else None
