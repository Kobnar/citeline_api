import mongoengine

from stackcite.data import utils


class MockDocument(utils.IDocument):
    """
    Provides a very basic data model to perform integration tests with MongoDB.
    This class can be sub-classed for specific test cases that require
    additional fields or methods.

    :cvar name: A unique string value.
    :cvar number: An arbitrary integer value.
    :cvar fact: An arbitrary boolean value.
    """
    name = mongoengine.StringField(required=True, unique=True)
    number = mongoengine.IntField()
    fact = mongoengine.BooleanField()

    meta = {
        'allow_inheritance': True,
        'indexes': [
            {
                'fields': ['$name'],
                'cls': False
            }
        ]
    }

    def _serialize(self, fields=()):
        return {
            'id': str(self.id) if self.id else None,
            'name': self.name,
            'number': self.number,
            'fact': self.fact
        }

    def _deserialize(self, data):
        for key, value in data.items():
            setattr(self, key, value)
