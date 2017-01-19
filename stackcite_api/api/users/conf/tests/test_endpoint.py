from stackcite_api import testing


class ConfirmationAPIEndpointTests(testing.endpoint.APIEndpointTestCase):

    def setUp(self):
        from stackcite import data as db
        db.User.drop_collection()
        db.ConfirmToken.drop_collection()
        super().setUp()

    def test_unauthenticated_user_can_create(self):
        """CREATE without authentication returns 200 OK
        """
        from stackcite import data as db
        db.User.new('test@email.com', 'T3stPa$$word', save=True)
        json_data = {'email': 'test@email.com'}
        response = self.test_app.post_json(
            '/v0/users/conf/',
            params=json_data,
            expect_errors=False)
        self.assertEqual(204, response.status_code)

    def test_unauthenticated_user_can_update(self):
        """UPDATE without authentication returns 200 OK
        """
        from stackcite import data as db
        user = db.User.new('test@email.com', 'T3stPa$$word', save=True)
        key = db.ConfirmToken.new(user, save=True).key
        json_data = {'key': key}
        response = self.test_app.put_json(
            '/v0/users/conf/',
            params=json_data,
            expect_errors=False)
        self.assertEqual(204, response.status_code)
