from marshmallow import fields

from citeline_api.api.schemas import fields as api_fields
from citeline_api.api.sources import schemas as source_schemas


class UpdateTextSource(source_schemas.UpdateSource):
    authors = api_fields.ListField()
    editors = fields.List(api_fields.ObjectIdField())


class CreateTextSource(UpdateTextSource):
    title = fields.String(required=True)
    authors = fields.List(api_fields.ObjectIdField(), required=True)
