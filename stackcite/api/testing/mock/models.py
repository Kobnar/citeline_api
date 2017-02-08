import mongoengine

from stackcite.data import utils


class MockDocument(utils.IDocument):
    """
    A "mock" collection definition designed for integration testing.
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
