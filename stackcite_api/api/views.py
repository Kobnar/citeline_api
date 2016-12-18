from pyramid.view import view_defaults

from stackcite_api.views import BaseView


@view_defaults(renderer='json')
class APIIndexViews(BaseView):
    """``/v{#}/``"""

    def index(self):
        """The main index view for the current version of the Stackcite API
        """
        return {
            'title': 'Stackcite API',
            'version': '0.0'
        }
