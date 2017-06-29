import logging
import mongoengine
from pyramid import security as sec

from stackcite import data as db

from stackcite.api import resources

from . import views, schema

_LOG = logging.getLogger(__name__)


class ConfirmationResource(
    resources.APIIndexResource,
    resources.SerializableResource):

    _VIEW_CLASS = views.ConfirmationViews

    __acl__ = [
        (sec.Allow, sec.Everyone, ('create', 'update'))
    ]

    _SCHEMA = schema.ConfirmToken

    def create(self, data):
        """
        Issues a new account confirmation token. Replaces an existing token if
        one already exists in the database.
        """
        email = data['email']
        user = db.User.objects.get(email=email)
        token = db.ConfirmToken.new(user)
        try:
            token.save()
        except mongoengine.NotUniqueError:
            db.ConfirmToken.objects(_user=user).delete()
            token.save()
        _LOG.info('Confirmation key: {} {}'.format(user.email, token.key))
        return token

    def update(self, data):
        """
        Confirms a user's registration.
        """
        key = data['key']
        token = db.ConfirmToken.objects.get(_key=key)
        user = token.confirm_user()
        _LOG.info('Confirmation key: {} {}'.format(user.email, token.key))
        return token
