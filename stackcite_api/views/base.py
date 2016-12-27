import functools
import mongoengine
import marshmallow

from stackcite_api import exceptions


def managed_view(view_method):
    """
    An exception manager for catching expected base exceptions in view methods
    and converting them into Pyramid-style API HTTP exceptions.
    """

    @functools.wraps(view_method)
    def wrapper(self, *args, **kwargs):
        try:
            return view_method(self, *args, **kwargs)

        except ValueError:
            msg = 'Failed to decode JSON body'
            raise exceptions.APIBadRequest(detail=msg)

        except marshmallow.ValidationError as err:
            msg = err.messages
            raise exceptions.APIBadRequest(detail=msg)

        except mongoengine.DoesNotExist:
            raise exceptions.APINotFound()

        except mongoengine.NotUniqueError:
            msg = 'Object already exists'
            raise exceptions.APIBadRequest(detail=msg)

        except mongoengine.ValidationError:
            msg = 'Object failed low-level validation'
            raise exceptions.APIBadRequest(detail=msg)

    return wrapper


class BaseView(object):
    """A basic view class.

    NOTE: Class is intended to be sub-classed for different pages.
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
