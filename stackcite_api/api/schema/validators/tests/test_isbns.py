import unittest

from stackcite_api import testing


class ISBN10ValidatorTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..isbns import ISBN10Validator
        self.validator = ISBN10Validator()

    def test_invalid_isbn10s_fail(self):
        """ISBN10Validator raises exception for invalid ISBNs
        """
        from marshmallow import ValidationError
        invalid_isbns = testing.data.invalid_isbns()
        for isbn in invalid_isbns:
            with self.assertRaises(ValidationError):
                self.validator(isbn)

    def test_valid_isbn10s_fail(self):
        """ISBN10Validator does not raise exception for valid ISBN-10s
        """
        from marshmallow import ValidationError
        valid_isbn10s = testing.data.valid_isbn10s()
        for isbn10 in valid_isbn10s:
            try:
                self.validator(isbn10)
            except ValidationError:
                msg = 'Valid ISBN-10 failed validation: {}'.format(isbn10)
                self.fail(msg)


class ISBN13ValidatorTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..isbns import ISBN13Validator
        self.validator = ISBN13Validator()

    def test_invalid_isbn10s_raise_exception(self):
        """ISBN13Validator raises exception for invalid ISBNs
        """
        from marshmallow import ValidationError
        invalid_isbns = testing.data.invalid_isbns()
        for isbn in invalid_isbns:
            with self.assertRaises(ValidationError):
                self.validator(isbn)

    def test_valid_isbn13s_do_not_raise_exception(self):
        """ISBN13Validator does not raise exception for valid ISBN-13s
        """
        from marshmallow import ValidationError
        valid_isbn13s = testing.data.valid_isbn13s()
        for isbn13 in valid_isbn13s:
            try:
                self.validator(isbn13)
            except ValidationError:
                msg = 'Valid ISBN-10 failed validation: {}'.format(isbn13)
                self.fail(msg)
