import unittest

from stackcite_api import testing


class RetrieveSourcesTests(unittest.TestCase):

    layer = testing.layers.UnitTestLayer

    def setUp(self):
        from ..schema import RetrieveSources
        self.schema = RetrieveSources()

    def test_accepts_q_field(self):
        """RetrieveSources accepts "q" field
        """
        data = {'q': 'Some query string.'}
        result, errors = self.schema.load(data)
        self.assertIn('q', result)
