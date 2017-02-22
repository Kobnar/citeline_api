from marshmallow import Schema, fields

from stackcite.api.schema import forms as api_forms


class UpdateOrganization(Schema):
    name = fields.String()
    established = fields.Integer(allow_none=True)
    description = fields.String()


class CreateOrganization(Schema):
    name = fields.String(required=True)
    established = fields.Integer(allow_none=True)
    description = fields.String()


class RetrieveOrganizations(api_forms.RetrieveCollection):
    q = fields.String()


class UpdatePublisher(Schema):
    name = fields.String()
    established = fields.Integer()
    region = fields.String(validate=lambda r: len(r) == 2)
    description = fields.String()


class CreatePublisher(Schema):
    name = fields.String(required=True)
    established = fields.Integer()
    region = fields.String(validate=lambda r: len(r) == 2)
    description = fields.String()
