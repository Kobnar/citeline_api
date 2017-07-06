from stackcite.api import testing


class PersonCollectionViewsIntegrationTestCase(
        testing.views.CollectionViewTestCase):

    layer = testing.layers.MongoTestLayer

    # Define resource and view classes
    from ..resources import PersonCollection
    from stackcite.api.views import APICollectionViews
    RESOURCE_CLASS = PersonCollection
    VIEW_CLASS = APICollectionViews

    def make_view(self, name='people'):
        return super().make_view(name)

    def setUp(self):
        from stackcite.data import Person
        Person.drop_collection()

    def test_create_raises_exception_for_invalid_data(self):
        """PersonCollectionViews.create() raises APIBadRequest with invalid data
        """
        from stackcite.api.exceptions import APIBadRequest
        data = {'name': {'first': 'John', 'full': 'John Nobody Doe'}}
        view = self.make_view()
        view.request.json_body = data
        with self.assertRaises(APIBadRequest):
            view.create()

    def test_retrieve_raises_exception_for_invalid_data(self):
        """PersonCollectionViews.retrieve() raises APIBadRequest with invalid query
        """
        from stackcite.api.exceptions import APIBadRequest
        data = {'limit': -1}
        view = self.make_view()
        view.request.params = data
        with self.assertRaises(APIBadRequest):
            view.retrieve()


class PersonDocumentViewsIntegrationTestCase(
        testing.views.DocumentViewTestCase):

    layer = testing.layers.MongoTestLayer

    # Define resource and view classes
    from ..resources import PersonCollection
    from stackcite.api.views import APIDocumentViews
    RESOURCE_CLASS = PersonCollection
    VIEW_CLASS = APIDocumentViews

    def setUp(self):
        from stackcite.data import Person
        Person.drop_collection()

    def make_person(self, save=False):
        from random import randint
        from .test_resources import make_person as mk_prs
        people = testing.data.people()
        rand_idx = randint(0, len(people) - 1)
        person = mk_prs(people[rand_idx], save)
        return person

    def make_view(self, object_id=None, name='people'):
        return super().make_view(object_id, name)

    def test_retrieve_raises_exception_for_missing_person(self):
        """PersonDocumentViews.retrieve() raises APINotFound for missing person
        """
        from stackcite.api.exceptions import APINotFound
        view = self.make_view()
        with self.assertRaises(APINotFound):
            view.retrieve()

    def test_update_raises_exception_for_invalid_data(self):
        """PersonDocumentViews.update() raises APIBadRequest with invalid data
        """
        from stackcite.api.exceptions import APIBadRequest
        data = {'name': {'first': 'John', 'full': 'John Nobody Doe'}}
        person = self.make_person(save=True)
        view = self.make_view(person.id)
        view.request.json_body = data
        with self.assertRaises(APIBadRequest):
            view.update()

    def test_delete_raises_204_exception_for_deleted_person(self):
        """PersonDocumentViews.delete() raises APINoContent for deleted person
        """
        from stackcite.api.exceptions import APINoContent
        person = self.make_person(save=True)
        view = self.make_view(person.id)
        with self.assertRaises(APINoContent):
            view.delete()

    def test_delete_raises_404_exception_for_missing_person(self):
        """PersonDocumentViews.delete() raises APINotFound for missing person
        """
        from stackcite.api.exceptions import APINotFound
        view = self.make_view()
        with self.assertRaises(APINotFound):
            view.delete()
