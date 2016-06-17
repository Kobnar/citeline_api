import unittest

from citeline_api import testing


class UpdateNameUnitTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schemas import UpdateName
        self.schema = UpdateName(strict=True)

    def test_validate_names_raises_exception_if_full_name_and_sub_names_set(self):
        """UpdateName.validate_names() raises ValidationError if full name and sub-names are set
        """
        from marshmallow import ValidationError
        data = {
            'middle': 'Nobody',
            'full': 'John Nobody Doe'}
        with self.assertRaises(ValidationError):
            self.schema.load(data)

    def test_validate_names_accepts_full_name_only(self):
        """UpdateName.validate_names() does not raise ValidationError if only a full name is set
        """
        from marshmallow import ValidationError
        data = {'full': 'John Nobody Doe'}
        try:
            self.schema.load(data)
        except ValidationError as err:
            self.fail(err)


class CreateNameUnitTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schemas import CreateName
        self.schema = CreateName(strict=True)

    def test_validate_names_raises_exception_if_full_name_and_sub_names_set(self):
        """CreateName.validate_names() raises ValidationError if full name and sub-names are set
        """
        from marshmallow import ValidationError
        data = {
            'middle': 'Nobody',
            'full': 'John Nobody Doe'}
        with self.assertRaises(ValidationError):
            self.schema.load(data)

    def test_validate_names_raises_exception_if_critical_names_missing(self):
        """CreateName.validate_names() raises ValidationError if neither title, last or full are set
        """
        from marshmallow import ValidationError
        data = {
            'first': 'John',
            'middle': 'Nobody'}
        with self.assertRaises(ValidationError):
            self.schema.load(data)

    def test_validate_names_accepts_full_name_only(self):
        """UpdateName.validate_names() does not raise ValidationError if only a full name is set
        """
        from marshmallow import ValidationError
        data = {'full': 'John Nobody Doe'}
        try:
            self.schema.load(data)
        except ValidationError as err:
            self.fail(err)


class UpdatePersonUnitTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schemas import UpdatePerson
        self.schema = UpdatePerson(strict=True)

    def test_nested_update_name_schema_validates(self):
        """UpdatePerson.name validates an invalid name condition
        """
        from marshmallow import ValidationError
        data = {
            'name': {
                'first': 'John',
                'full': 'John Nobody Doe'}}
        with self.assertRaises(ValidationError):
            self.schema.load(data)


class CreatePersonUnitTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schemas import CreatePerson
        self.schema = CreatePerson(strict=True)

    def test_name_required(self):
        """CreatePerson requires a name field to be set
        """
        from marshmallow import ValidationError
        data = {'description': 'A man with no name.'}
        with self.assertRaises(ValidationError):
            self.schema.load(data)

    def test_nested_update_name_schema_validates(self):
        """CreatePerson.name validates an invalid name condition
        """
        from marshmallow import ValidationError
        data = {
            'name': {
                'first': 'John',
                'middle': 'Nobody'}}
        with self.assertRaises(ValidationError):
            self.schema.load(data)
