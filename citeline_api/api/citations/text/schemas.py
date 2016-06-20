from marshmallow import fields

from citeline_api.api.schemas import fields as api_fields
from citeline_api.api.citations import schemas as citation_schemas


class UpdateTextCitation(citation_schemas.UpdateCitation):
    text = fields.String(required=True)


class CreateTextCitation(UpdateTextCitation):
    source = api_fields.ObjectIdField(required=True)
