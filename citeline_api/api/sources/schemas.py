from marshmallow import Schema, fields, validates, ValidationError

from citeline import data as db


class UpdateSource(Schema):
    title = fields.String()
    medium = fields.String(default='PRINT')
    description = fields.String()

    @validates('medium')
    def validate_medium(self, data):
        if data not in db.Source.MEDIUMS:
            msg = '{} is an invalid medium'
            raise ValidationError(msg.format(data))


class CreateSource(UpdateSource):
    title = fields.String(required=True)
