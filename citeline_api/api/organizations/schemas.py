from marshmallow import Schema, fields


class UpdateOrganization(Schema):
    name = fields.String()
    established = fields.Integer()


class CreateOrganization(UpdateOrganization):
    name = fields.String(required=True)
