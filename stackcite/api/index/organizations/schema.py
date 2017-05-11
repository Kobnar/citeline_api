from marshmallow import Schema, fields

from stackcite.api.schema import (
    fields as api_fields,
    api as api_forms
)


class Organization(Schema):
    id = api_fields.ObjectIdField()
    name = fields.String()
    established = fields.Integer(allow_none=True)
    description = fields.String()


class Publisher(Organization):
    region = fields.String(validate=lambda r: len(r) == 2)


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
