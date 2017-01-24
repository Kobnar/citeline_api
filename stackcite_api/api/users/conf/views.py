from stackcite_api import views, exceptions


class ConfirmationViews(views.BaseView):
    """``../conf/``"""

    METHODS = {
        'POST': 'create',
        'PUT': 'update',
    }

    @views.managed_view
    def create(self):
        data = self.request.json_body
        self.context.create(data)
        return exceptions.APINoContent()

    @views.managed_view
    def update(self):
        data = self.request.json_body
        self.context.update(data)
        return exceptions.APINoContent()
