from stackcite_api import testing


class AuthAPIEndpointTests(testing.endpoint.APIEndpointTestCase):

    def setUp(self):
        from stackcite.data import Token, User
        Token.drop_collection()
        User.drop_collection()
        self.test_app = self.make_app()

    @staticmethod
    def make_user(email, password, groups=(), save=False):
        from stackcite import data as db
        user = db.User()
        user.email = email
        user.set_password(password)
        for g in groups:
            user.add_group(g)
        if save:
            user.save()
        return user

    def auth_user(self, email, password):
        import json
        auth_data = {
            'email': email,
            'password': password}
        response = self.test_app.post(
            '/v0/auth/',
            content_type='applicaiton/json',
            params=json.dumps(auth_data),
            expect_errors=True)
        return response.json_body['key']


class CreateTokenAPIEndpointTests(AuthAPIEndpointTests):

    def test_create_token_returns_400_with_invalid_json_body(self):
        """CREATE 'auth/' returns 400 BAD REQUEST with invalid JSON data
        """
        json_data = '{"this": {horrible": data}'

        response = self.test_app.post(
            '/v0/auth/',
            content_type='applicaiton/json',
            params=json_data,
            expect_errors=True)
        result = response.status_code
        self.assertEqual(400, result)

    def test_crate_token_returns_400_with_invalid_credentials(self):
        """CREATE 'auth/' returns 400 BAD REQUEST with invalid credentials
        """
        import json
        auth_data = {
            'email': 'test@email.com',
            'password': 'T#stPa55word'}
        bad_auth_data = {
            'email': 'test@email.com',
            'password': 'bad_password'}

        self.make_user(auth_data['email'], auth_data['password'], save=True)

        response = self.test_app.post(
            '/v0/auth/',
            content_type='applicaiton/json',
            params=json.dumps(bad_auth_data),
            expect_errors=True)
        result = response.status_code
        self.assertEqual(400, result)

    def test_crate_token_returns_201_with_valid_credentials(self):
        """CREATE 'auth/' returns 201 CREATED with valid credentials
        """
        import json
        auth_data = {
            'email': 'test@email.com',
            'password': 'T#stPa55word'}

        self.make_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        response = self.test_app.post(
            '/v0/auth/',
            content_type='applicaiton/json',
            params=json.dumps(auth_data))
        result = response.status_code
        self.assertEqual(201, result)

    def test_retrieve_token_returns_403_with_invalid_key(self):
        """GET 'auth/' returns 403 FORBIDDEN with invalid key
        """
        key = 'invalid_key'
        response = self.test_app.get(
            '/v0/auth/',
            headers={'Authorization': 'key {}'.format(key)},
            expect_errors=True)
        result = response.status_code
        self.assertEqual(403, result)

    def test_retrieve_token_returns_200_with_valid_key(self):
        """GET 'auth/' returns 200 OK with valid key
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T#stPa55word'}

        self.make_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        key = self.auth_user(
            auth_data['email'],
            auth_data['password'])

        response = self.test_app.get(
            '/v0/auth/',
            headers={'Authorization': 'key {}'.format(key)},
            expect_errors=True)
        result = response.status_code
        self.assertEqual(200, result)

    def test_update_token_returns_403_with_invalid_key(self):
        """PUT 'auth/' returns 403 FORBIDDEN with invalid key
        """
        key = 'invalid_key'
        response = self.test_app.put(
            '/v0/auth/',
            headers={'Authorization': 'key {}'.format(key)},
            expect_errors=True)
        result = response.status_code
        self.assertEqual(403, result)

    def test_update_token_returns_200_with_valid_key(self):
        """PUT 'auth/' returns 200 OK with valid key
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T#stPa55word'}

        self.make_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        key = self.auth_user(
            auth_data['email'],
            auth_data['password'])

        response = self.test_app.put(
            '/v0/auth/',
            headers={'Authorization': 'key {}'.format(key)},
            expect_errors=True)
        result = response.status_code
        self.assertEqual(200, result)

    def test_delete_token_returns_403_with_invalid_key(self):
        """DELETE 'auth/' returns 403 FORBIDDEN with invalid key
        """
        key = 'invalid_key'
        response = self.test_app.delete(
            '/v0/auth/',
            headers={'Authorization': 'key {}'.format(key)},
            expect_errors=True)
        result = response.status_code
        self.assertEqual(403, result)

    def test_delete_token_returns_201_with_valid_key(self):
        """DELETE 'auth/' returns 204 NO CONTENT with valid key
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T#stPa55word'}

        self.make_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        key = self.auth_user(
            auth_data['email'],
            auth_data['password'])

        response = self.test_app.delete(
            '/v0/auth/',
            headers={'Authorization': 'key {}'.format(key)},
            expect_errors=True)
        result = response.status_code
        self.assertEqual(204, result)
