from marshmallow import Schema, fields

from citeline_api.api.schemas import fields as api_fields


class UpdateCitation(Schema):
    source = api_fields.ObjectIdField()
    note = fields.String()


class CreateCitation(UpdateCitation):
    source = api_fields.ObjectIdField(required=True)
