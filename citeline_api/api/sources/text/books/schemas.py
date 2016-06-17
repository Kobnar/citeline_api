from marshmallow import fields

from citeline_api.api.schemas import fields as api_fields
from citeline_api.api.sources import schemas as source_schemas


class UpdateBookSource(source_schemas.UpdateSource):
    edition = fields.String()
    publisher = api_fields.ObjectIdField()
    published = fields.Integer()
    location = fields.String()
    isbn10 = api_fields.ISBN10Field()
    isbn13 = api_fields.ISBN13Field()


class CreateBookSource(UpdateBookSource):
    title = fields.String(required=True)
    authors = fields.List(api_fields.ObjectIdField(), required=True)
