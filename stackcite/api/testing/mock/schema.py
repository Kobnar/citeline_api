from marshmallow import Schema, fields

from stackcite.api import schema


class MockDocumentSchema(Schema):
    id = schema.fields.ObjectIdField()
    name = fields.String()
    number = fields.Integer()
    fact = fields.Boolean()


class MockUpdateDocumentSchema(Schema):
    name = fields.String()
    number = fields.Integer()
    fact = fields.Boolean()


class MockCreateDocumentSchema(MockUpdateDocumentSchema):
    name = fields.String(required=True)


class MockRetrieveCollectionSchema(schema.forms.RetrieveCollection):
    name = fields.String()
    number = fields.Integer()
    fact = fields.Boolean()
