from stackcite.data.json import auth as _auth

from .utils import get_token, get_user
from .policies import AuthTokenAuthenticationPolicy

GROUPS = _auth.GROUPS
USERS, STAFF, ADMIN = GROUPS
