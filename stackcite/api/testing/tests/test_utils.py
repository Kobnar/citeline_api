import unittest

from stackcite.api import testing


class CreateUserTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from stackcite import data as db
        db.User.drop_collection()

    def test_adds_specified_groups(self):
        """create_user() adds specifically defined groups
        """
        from stackcite.api import auth
        expected = [auth.USERS, auth.STAFF]
        from ..utils import create_user
        user = create_user('test@email.com', 'T3stPa$$word', expected)
        result = user.groups
        self.assertEqual(expected, result)

    def test_saves_nothing_if_not_specified(self):
        """create_user() saves nothing to database by default
        """
        from ..utils import create_user
        create_user('test@email.com', 'T3stPa$$word')
        from stackcite import data as db
        result = db.User.objects().count()
        self.assertEqual(0, result)

    def test_saves_user_if_specified(self):
        """create_user() saves user to database if 'save=True'
        """
        from ..utils import create_user
        create_user('test@email.com', 'T3stPa$$word', save=True)
        from stackcite import data as db
        result = db.User.objects().count()
        self.assertEqual(1, result)


class CreateSourceTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from stackcite import data as db
        db.Source.drop_collection()

    def test_sets_title(self):
        """create_source() sets the title of the source
        """
        expected = 'Test Source'
        from ..utils import create_source
        source = create_source(expected)
        result = source.title
        self.assertEqual(expected, result)

    def test_saves_nothing_if_not_specified(self):
        """create_source() saves nothing by default
        """
        title = 'Test Source'
        from ..utils import create_source
        create_source(title)
        from stackcite import data as db
        result = db.Source.objects().count()
        self.assertEqual(0, result)

    def test_saves_source_if_specified(self):
        """create_source() saves source to database if 'save=True'
        """
        title = 'Test Source'
        from ..utils import create_source
        create_source(title, save=True)
        from stackcite import data as db
        result = db.Source.objects().count()
        self.assertEqual(1, result)


class CreateCitationTestCase(unittest.TestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    def setUp(self):
        from stackcite import data as db
        db.Citation.drop_collection()

    def test_sets_source(self):
        """create_citation() sets reference to given source
        """
        from ..utils import create_source
        source = create_source('Test Source')
        from ..utils import create_citation
        citation = create_citation(source)
        result = citation.source
        self.assertIs(source, result)

    def test_saves_nothing_if_not_specified(self):
        """create_citation() saves nothing by default
        """
        from .. import utils
        source = utils.create_source('Test Source')
        utils.create_citation(source)
        from stackcite import data as db
        result = db.Citation.objects().count()
        self.assertEqual(0, result)

    def test_saves_source_if_specified(self):
        """create_citation() saves citation to database if 'save=True'
        """
        from .. import utils
        source = utils.create_source('Test Source', save=True)
        utils.create_citation(source, save=True)
        from stackcite import data as db
        result = db.Citation.objects().count()
        self.assertEqual(1, result)
