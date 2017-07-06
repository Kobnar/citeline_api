"""
The Stackcite API comes equipped with a basic library of mock resources,
schema, etc. to perform integration and functional tests without relying on
the external Stackcite Database library.
"""

from .models import MockDocument
from .resources import (
    MockIndexResource,
    MockDocumentResource,
    MockCollectionResource,
    MockAPIIndexResource,
    MockAPIDocumentResource,
    MockAPICollectionResource
)
from .schema import MockDocumentSchema
from .utils import create_mock_data
