from marshmallow import Schema, fields

from stackcite.api.schema import forms as api_forms


class UpdateOrganization(Schema):
    name = fields.String()
    established = fields.Integer()


class CreateOrganization(Schema):
    name = fields.String(required=True)
    established = fields.Integer()


class RetrieveOrganizations(api_forms.RetrieveCollection):
    q = fields.String()


class UpdatePublisher(Schema):
    name = fields.String()
    established = fields.Integer()
    region = fields.String(validate=lambda r: len(r) == 2)


class CreatePublisher(Schema):
    name = fields.String(required=True)
    established = fields.Integer()
    region = fields.String(validate=lambda r: len(r) == 2)
