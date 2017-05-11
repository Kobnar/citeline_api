from marshmallow import fields

from stackcite.api import schema


class MockDocumentSchema(schema.APISchema):
    id = schema.fields.ObjectIdField()
    name = fields.String()
    number = fields.Integer()
    fact = fields.Boolean()


class MockUpdateDocumentSchema(schema.APISchema):
    name = fields.String()
    number = fields.Integer()
    fact = fields.Boolean()


class MockCreateDocumentSchema(MockUpdateDocumentSchema):
    name = fields.String(required=True)


class MockRetrieveCollectionSchema(schema.RetrieveCollection):
    name = fields.String()
    number = fields.Integer()
    fact = fields.Boolean()


class MockRetrieveDocumentSchema(schema.RetrieveDocument):
    pass
