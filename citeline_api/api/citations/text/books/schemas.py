from marshmallow import fields

from citeline_api.api.schemas import fields as api_fields
from citeline_api.api.citations.text import schemas as text_schemas


class UpdateBookCitation(text_schemas.UpdateTextCitation):
    pages = fields.List(fields.Integer())


class CreateBookCitation(UpdateBookCitation):
    source = api_fields.ObjectIdField(required=True)
    text = fields.String(required=True)
