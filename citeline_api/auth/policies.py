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

    def __init__(self, callback, debug=False):
        # self.callback = callback
        self.debug = debug

    # TODO: Working with Pyramid's callback pattern has proven nontrivial...
    def callback(self, user_id, request):
        return utils.get_groups(user_id, request)

    def unauthenticated_userid(self, request):
        """
        Resolves a :class:`citeline.Token` key to retrieve the
        :class:`bson.ObjectId` of a :class:`citeline.User`. If the token
        does not exist, method returns `None`.
        """
        return request.user.id if request.user else None
