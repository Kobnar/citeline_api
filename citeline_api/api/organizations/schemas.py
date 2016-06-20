from marshmallow import Schema, fields


class UpdateOrganization(Schema):
    name = fields.String()
    established = fields.Integer()


class CreateOrganization(Schema):
    name = fields.String(required=True)
    established = fields.Integer()


class UpdatePublisher(Schema):
    name = fields.String()
    established = fields.Integer()
    region = fields.String(validate=lambda r: len(r) == 2)


class CreatePublisher(Schema):
    name = fields.String(required=True)
    established = fields.Integer()
    region = fields.String(validate=lambda r: len(r) == 2)
