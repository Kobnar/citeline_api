from stackcite_api import views


class APIIndexViews(views.APIIndexViews):
    """``/v{#}/``"""

    def retrieve(self):
        return {
            'title': 'Stackcite API',
            'version': '0.0'
        }
