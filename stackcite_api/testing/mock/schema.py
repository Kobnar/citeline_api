from marshmallow import Schema, fields


class MockUpdateDocumentSchema(Schema):
    name = fields.String()
    number = fields.Integer()
    fact = fields.Boolean()


class MockCreateDocumentSchema(MockUpdateDocumentSchema):
    name = fields.String(required=True)
