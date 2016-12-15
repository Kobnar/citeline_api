from stackcite_api import testing


class AuthViewsTests(testing.views.CollectionViewTestCase):

    layer = testing.layers.MongoIntegrationTestLayer

    # Define resource and view class under test
    from ..resources import AuthResource
    from ..views import AuthViews
    RESOURCE_CLASS = AuthResource
    VIEW_CLASS = AuthViews

    def setUp(self):
        from stackcite import data as db
        db.Token.drop_collection()
        db.User.drop_collection()
        super().setUp()

    def get_view(self, name='api_v1'):
        return super().get_view(name)

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


class AuthViewsCreateTests(AuthViewsTests):

    def test_create_success_returns_201(self):
        """AuthViews.create() success returns 201 CREATED
        """
        data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}
        self.make_user(data['email'], data['password'], save=True)
        view = self.get_view()
        view.request.json_body = data
        view.create()
        result = view.request.response.status_code
        self.assertEqual(201, result)

    def test_create_invalid_data_returns_400(self):
        """AuthViews.create() with invalid data raises 400 BAD REQUEST
        """
        from stackcite_api.api import exceptions as exc
        data = {
            'cats': 'Are evil.',
            'dogs': 'Are lovely.'}
        self.make_user('test@email.com', 'T3stPa$$word', save=True)
        view = self.get_view()
        view.request.json_body = data
        with(self.assertRaises(exc.APIBadRequest)):
            view.create()

    def test_create_no_user_returns_400(self):
        """AuthViews.create() with unregistered user raises 400 BAD REQUEST
        """
        from stackcite_api.api import exceptions as exc
        data = {
            'email': 'wrong@email.com',
            'password': 'T3stPa$$word'}
        self.make_user('test@email.com', data['password'], save=True)
        view = self.get_view()
        view.request.json_body = data
        with(self.assertRaises(exc.APIBadRequest)):
            view.create()

    def test_create_wrong_password_returns_400(self):
        """AuthViews.create() with wrong password raises 400 BAD REQUEST
        """
        from stackcite_api.api import exceptions as exc
        data = {
            'email': 'test@email.com',
            'password': 'T3stPa$$word'}
        self.make_user(data['email'], 'B4dPa$$word', save=True)
        view = self.get_view()
        view.request.json_body = data
        with(self.assertRaises(exc.APIBadRequest)):
            view.create()
