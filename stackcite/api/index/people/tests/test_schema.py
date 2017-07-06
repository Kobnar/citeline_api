import unittest

from stackcite.api import testing


class NameSchemaTests(unittest.TestCase):

    layer = testing.layers.BaseTestLayer

    def setUp(self):
        from ..schema import Name
        self.schema = Name(strict=True)


class NameSchemaCreateTests(NameSchemaTests):

    def setUp(self):
        super().setUp()
        self.schema.method = 'POST'

    def test_load_raises_exception_if_full_name_and_sub_names_set(self):
        """Name.load() raises ValidationError when creating conflicting names
        """
        from marshmallow import ValidationError
        data = {
            'middle': 'Nobody',
            'full': 'John Nobody Doe'}
        with self.assertRaises(ValidationError):
            self.schema.load(data)

    def test_load_raises_exception_if_critical_names_missing(self):
        """Name.load() raises ValidationError when creating missing names
        """
        from marshmallow import ValidationError
        data = {
            'first': 'John',
            'middle': 'Nobody'}
        with self.assertRaises(ValidationError):
            self.schema.load(data)

    def test_load_full_name_only(self):
        """Name.load() does not raise exception when creating full name only
        """
        from marshmallow import ValidationError
        data = {'full': 'John Nobody Doe'}
        try:
            self.schema.load(data)
        except ValidationError as err:
            self.fail(err)


class NameSchemaUpdateTests(NameSchemaTests):

    def setUp(self):
        super().setUp()
        self.schema.method = 'PUT'

    def test_load_raises_exception_if_full_name_and_sub_names_set(self):
        """Name.load() raises ValidationError when updating conflicting names
        """
        from marshmallow import ValidationError
        data = {
            'middle': 'Nobody',
            'full': 'John Nobody Doe'}
        with self.assertRaises(ValidationError):
            self.schema.load(data)

    def test_load_full_name_only(self):
        """Name.load() does not raise exception when updating full name only
        """
        from marshmallow import ValidationError
        data = {'full': 'John Nobody Doe'}
        try:
            self.schema.load(data)
        except ValidationError as err:
            self.fail(err)


class PersonSchemaTests(unittest.TestCase):

    layer = testing.layers.BaseTestLayer

    def setUp(self):
        from ..schema import Person
        self.schema = Person(strict=True)


class PersonSchemaCreateTests(PersonSchemaTests):

    def setUp(self):
        super().setUp()
        self.schema.method = 'POST'

    def test_name_required(self):
        """Person.load() requires a name field to be set on POST
        """
        from marshmallow import ValidationError
        data = {'description': 'A man with no name.'}
        with self.assertRaises(ValidationError):
            self.schema.load(data)

    def test_nested_update_name_schema_validates(self):
        """CreatePerson.name validates an invalid name condition on POST
        """
        from marshmallow import ValidationError
        data = {
            'name': {
                'first': 'John',
                'middle': 'Nobody'}}
        with self.assertRaises(ValidationError):
            self.schema.load(data)

    def test_birth_allows_none(self):
        """CreatePerson.birth accepts None value on POST
        """
        data = {
            'name': {'title': 'J.N. Doe'},
            'birth': None}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('birth', result)

    def test_death_allows_none(self):
        """CreatePerson.death accepts None value on POST
        """
        data = {
            'name': {'title': 'J.N. Doe'},
            'birth': None}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('death', result)


class PersonSchemaUpdateTests(PersonSchemaTests):

    def setUp(self):
        super().setUp()
        self.schema.method = 'PUT'

    def test_nested_update_name_schema_validates(self):
        """Person.name validates an invalid name condition on PUT
        """
        from marshmallow import ValidationError
        data = {
            'name': {
                'first': 'John',
                'full': 'John Nobody Doe'}}
        with self.assertRaises(ValidationError):
            self.schema.load(data)

    def test_birth_allows_none(self):
        """UpdatePerson.birth accepts None value on PUT
        """
        data = {'birth': None}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('birth', result)

    def test_death_allows_none(self):
        """UpdatePerson.death accepts None value on PUT
        """
        data = {'death': None}
        result = self.schema.load(data).errors.keys()
        self.assertNotIn('death', result)
