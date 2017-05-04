import functools
import mongoengine
import marshmallow
import json

from pyramid import exceptions as exc

from pyramid.view import (
    view_config,
    view_defaults,
    forbidden_view_config,
    notfound_view_config
)

from stackcite.api import exceptions

from . import base


def managed_view(view_method):
    """
    An exception manager for catching expected base exceptions in view methods
    and converting them into Pyramid-style API HTTP exceptions.
    """

    @functools.wraps(view_method)
    def wrapper(self, *args, **kwargs):
        try:
            return view_method(self, *args, **kwargs)

        except (ValueError, json.JSONDecodeError):
            raise exceptions.APIDecodingError()

        except marshmallow.ValidationError as err:
            errors = err.messages
            raise exceptions.APIValidationError(detail=errors)

        except mongoengine.DoesNotExist:
            raise exceptions.APINotFound()

        except mongoengine.NotUniqueError:
            raise exceptions.APINotUniqueError()

        except mongoengine.ValidationError as err:
            errors = err.to_dict()
            raise exceptions.APIValidationError(detail=errors)

    return wrapper


@view_defaults(renderer='json')
class APIExceptionViews(base.BaseView):
    """
    A view class to provide JSON formatted exceptions.
    """

    @forbidden_view_config()
    @notfound_view_config()
    @view_config(context=exc.HTTPBadRequest)
    @view_config(context=exceptions.APIConflict)
    def exception(self):
        self.request.response.status_code = self.context.code

        # TODO: Replace manual overrides with exception class instantiation

        # Override exception detail for 403 Forbidden errors
        if self.context.code == exceptions.APIForbidden.code:
            self.context.detail = {}

        # Override exception detail for 404 NotFound errors
        if self.context.code == exceptions.APINotFound.code:
            self.context.detail = {'path': self.context.detail}

        return {
            'code': self.context.code,
            'title': self.context.title,
            'explanation': self.context.explanation,
            'detail': self.context.detail or {}
        }


@view_defaults(renderer='json')
class APIIndexViews(base.BaseView):
    """
    A base view class providing empty API index views that do not perform any
    CRUD operations.
    """

    METHODS = {
        'GET': 'retrieve'
    }

    def retrieve(self):
        raise exceptions.APINoContent()


@view_defaults(renderer='json')
class APICollectionViews(base.BaseView):
    """
    A base view class to CREATE and RETRIEVE documents from a MongoDB
    collection using v.1 of the Stackcite API.

    NOTE: Object serialization is handled by the traversal resource, not the
    view object. By the time the object is handled by the view object, it has
    already been serialized into a nested dictionary representation of data.
    """

    METHODS = {
        'POST': 'create',
        'GET': 'retrieve'
    }

    @managed_view
    def create(self):
        """CREATE a new document using JSON data from the request body.

        :return dict: A dictionary containing the new document's ``ObjectId``
        """
        data = self.request.json_body
        self.request.response.status = 201
        data, errors = self.context.load('POST', data)
        result = self.context.create(data)
        return result.serialize()

    @managed_view
    def retrieve(self):
        """
        RETRIEVE a list of documents matching the provided query (if any).

        :return: A list of serialized documents matching query parameters (if any)
        """
        query = self.request.params
        query, errors = self.context.load('GET', query)
        query, params = self.context.get_params(query)
        results = self.context.retrieve(query)
        return {
            'count': results.count(),
            'limit': params['limit'],
            'skip': params['skip'],
            'items': [doc.serialize(params['fields']) for doc in results]
        }


@view_defaults(renderer='json')
class APIDocumentViews(base.BaseView):
    """
    A base view class to RETRIEVE, UPDATE and DELETE documents from a MongoDB
    collection using v.1 of the Stackcite API
    """

    METHODS = {
        'GET': 'retrieve',
        'PUT': 'update',
        'DELETE': 'delete'
    }

    @managed_view
    def retrieve(self):
        """RETRIEVE an individual document

        :return: A serialized version of the document
        """
        query = self.request.params
        query, errors = self.context.load('GET', query)
        query, params = self.context.get_params(query)
        results = self.context.retrieve(query)
        return results.serialize(params['fields'])

    @managed_view
    def update(self):
        """
        UPDATE an individual document using JSON data from the request.

        Raises ``404 NOT FOUND`` if the document does not exist or ``400 BAD
        REQUEST`` if there is some other problem with the request (e.g. schema
        validation error).

        :return: A serialized version of the updated document
        """
        data = self.request.json_body
        data, errors = self.context.load('PUT', data)
        result = self.context.update(data)
        return result.serialize()

    @managed_view
    def delete(self):
        """
        DELETE an individual document.

        Raises ``204 NO CONTENT`` if successful or ``404 NOT FOUND`` if
        document does not exist.
        """
        self.context.delete()
        raise exceptions.APINoContent()
