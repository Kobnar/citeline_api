"""
This package contains a number of utilities designed to facilitate a standard
setup and teardown procedure for various components of the Stackcite API.
"""

from stackcite.data.testing import data as _data

from . import endpoint
from . import layers
from . import mock
from . import utils
from . import views

data = _data
