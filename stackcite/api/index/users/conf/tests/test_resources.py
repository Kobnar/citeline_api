import unittest

from stackcite.api import testing


class ConfirmationResourceTestCase(unittest.TestCase):

    layer = testing.layers.MongoTestLayer

    def setUp(self):
        from stackcite import data as db
        db.User.drop_collection()
        db.ConfirmToken.drop_collection()
        from ..resources import ConfirmationResource
        self.collection = ConfirmationResource(None, 'confirmation')


class ConfirmationResourceCreateTestCase(ConfirmationResourceTestCase):

    def test_unknown_user_raises_exception(self):
        """ConfirmationResource.create() raises exception for an unknown user
        """
        data = {'email': 'test@email.com'}
        import mongoengine
        with self.assertRaises(mongoengine.DoesNotExist):
            self.collection.create(data)

    def test_new_token_created_in_db(self):
        """ConfirmationResource.create() creates a new confirmation token
        """
        from stackcite import data as db
        user = db.User.new('test@email.com', 'T3stPa$$word', save=True)
        data = {'email': user.email}
        self.collection.create(data)
        import mongoengine
        try:
            db.ConfirmToken.objects.get(_user=user)
        except mongoengine.DoesNotExist as err:
            self.fail(err)

    def test_existing_token_replaced_in_db(self):
        """ConfirmationResource.create() creates a new confirmation token if one exists
        """
        from stackcite import data as db
        user = db.User.new('test@email.com', 'T3stPa$$word', save=True)
        prev_key = db.ConfirmToken.new(user, save=True).key
        data = {'email': user.email}
        new_key = self.collection.create(data).key
        expected = [prev_key, new_key]
        results = [t.key for t in db.ConfirmToken.objects(_user=user)]
        self.assertEqual(expected, results)

    def test_returns_confirm_token(self):
        """ConfirmationResource.create() returns a ConfirmToken
        """
        from stackcite import data as db
        user = db.User.new('test@email.com', 'T3stPa$$word', save=True)
        data = {'email': user.email}
        result = self.collection.create(data)
        self.assertIsInstance(result, db.ConfirmToken)


class ConfirmationResourceUpdateTestCase(ConfirmationResourceTestCase):

    def test_unknown_key_raises_exception(self):
        """ConfirmationResource.update() raises exception for unknown key
        """
        from stackcite import data as db
        unknown_key = db.utils.gen_key()
        data = {'key': unknown_key}
        import mongoengine
        with self.assertRaises(mongoengine.DoesNotExist):
            self.collection.update(data)

    def test_sets_user_confirmed_in_db(self):
        """ConfirmationResource.update() confirms a known user account
        """
        from stackcite import data as db
        user = db.User.new('test@email.com', 'T3stPa$$word', save=True)
        key = db.ConfirmToken.new(user, save=True).key
        data = {'key': key}
        self.collection.update(data)
        result = db.User.objects.get(id=user.id).confirmed
        self.assertIsNotNone(result)

    def test_deletes_token(self):
        """ConfirmationResource.update() deletes existing token if successful
        """
        from stackcite import data as db
        user = db.User.new('test@email.com', 'T3stPa$$word', save=True)
        key = db.ConfirmToken.new(user, save=True).key
        data = {'key': key}
        self.collection.update(data)
        import mongoengine
        with self.assertRaises(mongoengine.DoesNotExist):
            db.ConfirmToken.objects.get(_key=key)

    def test_returns_confirm_token(self):
        """ConfirmationResource.update() returns 'True' if successful
        """
        from stackcite import data as db
        user = db.User.new('test@email.com', 'T3stPa$$word', save=True)
        key = db.ConfirmToken.new(user, save=True).key
        data = {'key': key}
        result = self.collection.update(data)
        self.assertTrue(result)

