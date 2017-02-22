from marshmallow import Schema, fields, validates_schema, ValidationError

from stackcite import data as db

from stackcite.api.schema import (
    fields as api_fields,
    forms as api_forms
)


class _UpdateSource(object):
    source_type = fields.String(load_from='type')
    title = fields.String()
    description = fields.String(allow_none=True)


class _CreateSource(_UpdateSource):
    source_type = fields.String(
        load_from='type',
        missing='SOURCE',
        required=True,
        validate=lambda t: t in db.Source.TYPES)
    title = fields.String(required=True)


class _UpdateTextSource(object):
    authors = fields.List(api_fields.ObjectIdField())
    editors = fields.List(api_fields.ObjectIdField())


class _CreateTextSource(_UpdateTextSource):
    @validates_schema
    def validate_authors(self, data):
        source_type = data.get('source_type')
        authors = data.get('authors')
        if source_type in ('TEXT', 'BOOK') and not authors:
            msg = 'Missing data for required field.'
            raise ValidationError(msg, ['authors'])


class _UpdateBookSource(object):
    edition = fields.String(allow_none=True)
    publisher = api_fields.ObjectIdField(allow_none=True)
    published = fields.Integer(allow_none=True)
    location = fields.String(allow_none=True)
    isbn10 = api_fields.ISBN10Field(allow_none=True)
    isbn13 = api_fields.ISBN13Field(allow_none=True)


class UpdateSource(
        Schema,
        _UpdateSource,
        _UpdateTextSource,
        _UpdateBookSource):
    pass


class CreateSource(
        Schema,
        _CreateSource,
        _CreateTextSource,
        _UpdateBookSource):
    pass


class RetrieveSources(api_forms.RetrieveCollection):
    q = fields.String()
