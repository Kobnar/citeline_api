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
            '/v0/users/confirmation/',
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
            '/v0/users/confirmation/',
            params=json_data,
            expect_errors=False)
        self.assertEqual(204, response.status_code)


class UsersAPIEndpointTests(testing.endpoint.APIEndpointTestCase):

    def setUp(self):
        from stackcite import data as db
        db.User.drop_collection()
        super().setUp()

    def auth_user(self, email, password):
        auth_data = {
            'email': email,
            'password': password}
        response = self.test_app.post_json(
            '/v0/auth/',
            params=auth_data,
            expect_errors=True)
        return response.json_body['key']


class UserCollectionAPIEndpointTests(UsersAPIEndpointTests):

    def test_create_invalid_json_body_returns_400(self):
        """CREATE with a malformed JSON body to `users/` returns 400 BAD REQUEST
        """
        json_data = '{"this": {horrible": data}'

        response = self.test_app.post_json(
            '/v0/users/',
            content_type='applicaiton/json',
            params=json_data,
            expect_errors=True)
        result = response.status_code
        self.assertEqual(400, result)

    def test_create_user_success_returns_201(self):
        """Successful POST to 'users/' returns 201 CREATED
        """
        json_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}

        response = self.test_app.post_json(
            '/v0/users/', params=json_data)
        result = response.status_code
        self.assertEqual(201, result)

    def test_create_valid_user_returns_valid_object_id(self):
        """Successful POST to 'users/' returns HTTP 201 status
        """
        import bson
        json_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}

        response = self.test_app.post_json(
            '/v0/users/', content_type='applicaiton/json', params=json_data)
        result = response.json_body['id']
        self.assertTrue(bson.ObjectId.is_valid(result))

    def test_create_invalid_user_password_returns_400(self):
        """Invalid password POST to 'users/' returns 400 BAD REQUEST
        """
        json_data = {
            'email': 'test@email.com',
            'password': 'TestPassword'}

        response = self.test_app.post_json(
            '/v0/users/',
            params=json_data,
            expect_errors=True)
        self.assertEqual(400, response.status_code)

    def test_unauthenticated_retrieve_users_returns_403(self):
        """Unauthenticated GET to 'users/' returns 403 FORBIDDEN
        """
        response = self.test_app.get(
            '/v0/users/',
            expect_errors=True)
        self.assertEqual(403, response.status_code)

    def test_authenticated_retrieve_users_returns_403(self):
        """Authenticated GET to 'users/' from group 'users' returns 403 FORBIDDEN
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}

        # Create a new user
        testing.utils.create_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        # Authenticate user
        key = self.auth_user(**auth_data)

        # Try to retrieve all users
        headers = {
            'Authorization': 'key {}'.format(key)
        }
        response = self.test_app.get(
            '/v0/users/',
            headers=headers,
            expect_errors=True)
        self.assertEqual(403, response.status_code)

    def test_authenticated_staff_retrieve_users_returns_403(self):
        """Authenticated GET to 'users/' from group 'staff' returns 403 FORBIDDEN
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}

        # Create a new staff user
        testing.utils.create_user(
            auth_data['email'],
            auth_data['password'],
            groups=['staff'],
            save=True)

        # Authenticate user
        key = self.auth_user(**auth_data)

        # Try to retrieve all users
        headers = {
            'Authorization': 'key {}'.format(key)
        }
        response = self.test_app.get(
            '/v0/users/',
            headers=headers,
            expect_errors=True)
        self.assertEqual(403, response.status_code)

    def test_authenticated_admin_retrieve_users_returns_200(self):
        """Authenticated GET to 'users/' from group 'admin' returns 200 OK
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}

        # Create a new admin user
        testing.utils.create_user(
            auth_data['email'],
            auth_data['password'],
            groups=['admin'],
            save=True)

        # Authenticate user
        key = self.auth_user(**auth_data)

        # Try to retrieve all users
        headers = {'Authorization': 'key {}'.format(key)}
        response = self.test_app.get(
            '/v0/users/',
            headers=headers)
        self.assertEqual(200, response.status_code)


class UserDocumentAPIEndpointTests(UsersAPIEndpointTests):

    def test_unauthenticated_retrieve_returns_403(self):
        """Unauthenticated GET to 'users/{id}/' returns 403 FORBIDDEN
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}

        # Create a new user
        user = testing.utils.create_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        # Try to view user data
        response = self.test_app.get(
            '/v0/users/{}/'.format(str(user.id)),
            expect_errors=True)
        self.assertEqual(403, response.status_code)

    def test_unauthenticated_update_returns_403(self):
        """Unauthenticated PUT to 'users/{id}/' returns 403 FORBIDDEN
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}

        # Create a new user
        user = testing.utils.create_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        # Try to update user data
        response = self.test_app.put_json(
            '/v0/users/{}/'.format(str(user.id)),
            expect_errors=True)
        self.assertEqual(403, response.status_code)

    def test_unauthenticated_delete_returns_403(self):
        """Unauthenticated DELETE to 'users/{id}/' returns 403 FORBIDDEN
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}

        # Create a new user
        user = testing.utils.create_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        # Try to delete user data
        response = self.test_app.delete(
            '/v0/users/{}/'.format(str(user.id)),
            expect_errors=True)
        self.assertEqual(403, response.status_code)

    def test_authenticated_retrieve_returns_200(self):
        """Authenticated GET to 'users/{id}/' returns 200 OK
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}

        # Create a new user
        user = testing.utils.create_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        # Authenticate user
        key = self.auth_user(**auth_data)

        # Try to view user data
        headers = {'Authorization': 'key {}'.format(key)}
        response = self.test_app.get(
            '/v0/users/{}/'.format(str(user.id)),
            headers=headers)
        self.assertEqual(200, response.status_code)

    def test_authenticated_update_returns_200(self):
        """Authenticated PUT to 'users/{id}/' returns 200 OK
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}
        new_data = {
            'email': 'changed@email.com'}

        # Create a new user
        user = testing.utils.create_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        # Authenticate user
        key = self.auth_user(**auth_data)

        # Try to update user data
        headers = {'Authorization': 'key {}'.format(key)}
        response = self.test_app.put_json(
            '/v0/users/{}/'.format(str(user.id)),
            headers=headers,
            params=new_data)
        self.assertEqual(200, response.status_code)

    def test_authenticatd_update_invalid_json_body_returns_400(self):
        """Authenticated PUT with a malformed JSON body to to 'users/{id}/' returns 400 BAD REQUEST
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}
        new_data = '{"this": {horrible": data}'

        # Create a new user
        user = testing.utils.create_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        # Authenticate user
        key = self.auth_user(**auth_data)

        # Try to update user data
        headers = {'Authorization': 'key {}'.format(key)}
        response = self.test_app.put(
            '/v0/users/{}/'.format(str(user.id)),
            headers=headers,
            params=new_data,
            expect_errors=True)
        self.assertEqual(400, response.status_code)

    def test_authenticated_delete_returns_200(self):
        """Authenticated DELETE to 'users/{id}/' returns 204 NO CONTENT
        """
        auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}

        # Create a new user
        user = testing.utils.create_user(
            auth_data['email'],
            auth_data['password'],
            save=True)

        # Authenticate user
        key = self.auth_user(**auth_data)

        # Try to view user data
        headers = {'Authorization': 'key {}'.format(key)}
        response = self.test_app.delete(
            '/v0/users/{}/'.format(str(user.id)),
            headers=headers)
        self.assertEqual(204, response.status_code)

    def test_authenticated_retrieve_other_user_returns_403(self):
        """Authenticated GET to a different 'users/{id}/' returns 403 FORBIDDEN
        """
        user_1_auth_data = {
            'email': 'user1@email.com',
            'password': 'T3stPa$$word'}
        user_2_auth_data = {
            'email': 'user2@email.com',
            'password': 'T3stPa$$word'}

        # Create a new user
        testing.utils.create_user(
            user_1_auth_data['email'],
            user_1_auth_data['password'],
            save=True)

        # Create a new admin user
        user_2 = testing.utils.create_user(
            user_2_auth_data['email'],
            user_2_auth_data['password'],
            save=True)

        # Authenticate user
        user_1_key = self.auth_user(**user_1_auth_data)

        # Try to view user data
        headers = {'Authorization': 'key {}'.format(user_1_key)}
        response = self.test_app.get(
            '/v0/users/{}/'.format(str(user_2.id)),
            headers=headers,
            expect_errors=True)
        self.assertEqual(403, response.status_code)

    def test_staff_retrieve_other_user_returns_403(self):
        """Staff GET to a different 'users/{id}/' returns 403 FORBIDDEN
        """
        user_auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}
        staff_auth_data = {
            'email': 'admin@email.com',
            'password': 'T3stPa$$word'}

        # Create a new user
        user = testing.utils.create_user(
            user_auth_data['email'],
            user_auth_data['password'],
            save=True)

        # Create a new admin user
        testing.utils.create_user(
            staff_auth_data['email'],
            staff_auth_data['password'],
            groups=['staff'],
            save=True)

        # Authenticate user
        staff_key = self.auth_user(**staff_auth_data)

        # Try to view user data
        headers = {'Authorization': 'key {}'.format(staff_key)}
        response = self.test_app.get(
            '/v0/users/{}/'.format(str(user.id)),
            headers=headers,
            expect_errors=True)
        self.assertEqual(403, response.status_code)

    def test_admin_retrieve_other_user_returns_200(self):
        """Admin GET to a different 'users/{id}/' returns 200 OK
        """
        user_auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}
        admin_auth_data = {
            'email': 'admin@email.com',
            'password': 'T3stPa$$word'}

        # Create a new user
        user = testing.utils.create_user(
            user_auth_data['email'],
            user_auth_data['password'],
            save=True)

        # Create a new admin user
        testing.utils.create_user(
            admin_auth_data['email'],
            admin_auth_data['password'],
            groups=['admin'],
            save=True)

        # Authenticate user
        admin_key = self.auth_user(**admin_auth_data)

        # Try to view user data
        headers = {'Authorization': 'key {}'.format(admin_key)}
        response = self.test_app.get(
            '/v0/users/{}/'.format(str(user.id)),
            headers=headers)
        self.assertEqual(200, response.status_code)

    def test_admin_update_other_user_returns_200(self):
        """Admin PUT to a different 'users/{id}/' returns 200 OK
        """
        import json
        user_auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}
        admin_auth_data = {
            'email': 'admin@email.com',
            'password': 'T3stPa$$word'}
        new_user_data = {
            'email': 'other@email.com'}

        # Create a new user
        user = testing.utils.create_user(
            user_auth_data['email'],
            user_auth_data['password'],
            save=True)

        # Create a new admin user
        testing.utils.create_user(
            admin_auth_data['email'],
            admin_auth_data['password'],
            groups=['admin'],
            save=True)

        # Authenticate user
        admin_key = self.auth_user(**admin_auth_data)

        # Try to view user data
        headers = {'Authorization': 'key {}'.format(admin_key)}
        response = self.test_app.put_json(
            '/v0/users/{}/'.format(str(user.id)),
            content_type='application/json',
            headers=headers,
            params=new_user_data)
        self.assertEqual(200, response.status_code)

    def test_admin_delete_other_user_returns_204(self):
        """Admin DELETE to a different 'users/{id}/' returns 204 OK
        """
        user_auth_data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}
        admin_auth_data = {
            'email': 'admin@email.com',
            'password': 'T3stPa$$word'}

        # Create a new user
        user = testing.utils.create_user(
            user_auth_data['email'],
            user_auth_data['password'],
            save=True)

        # Create a new admin user
        testing.utils.create_user(
            admin_auth_data['email'],
            admin_auth_data['password'],
            groups=['admin'],
            save=True)

        # Authenticate user
        admin_key = self.auth_user(**admin_auth_data)

        # Try to view user data
        headers = {'Authorization': 'key {}'.format(admin_key)}
        response = self.test_app.delete(
            '/v0/users/{}/'.format(str(user.id)),
            headers=headers)
        self.assertEqual(204, response.status_code)
