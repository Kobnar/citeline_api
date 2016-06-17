from marshmallow import fields

from citeline_api.api.organizations import schemas as api_schemas


class UpdatePublisher(api_schemas.UpdateOrganization):
    region = fields.String(validate=lambda r: len(r) == 2)


class CreatePublisher(UpdatePublisher):
    name = fields.String(required=True)
