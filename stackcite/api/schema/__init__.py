"""
The Stackcite API uses ``marshmallow`` for data validation and serialization.
In many cases, custom fields and schemas are implemented to provide common
features.
"""

from . import fields
from . import validators

from .schema import (
    APISchema,
    APIDocumentSchema,
    APICollectionSchema
)
