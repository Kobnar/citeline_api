from pyramid import httpexceptions


class APINoContent(httpexceptions.HTTPNoContent):
    """
    Subclass of :class:`~HTTPNoContent` used to raise HTTP exceptions within
    the API instead of forwarding the user to a front-end styled exception
    page.

    code: 204, title: No Content
    """


class APIBadRequest(httpexceptions.HTTPBadRequest):
    """
    Subclass of :class:`~HTTPBadRequest` used to raise HTTP exceptions within
    the API instead of forwarding the user to a front-end styled exception
    page.

    code: 400, title: Bad Request
    """


class APIDecodingError(APIBadRequest):
    """
    Subclass of :class:`~APIBadReqeust` used to set a custom explanation for
    `ValueError` exceptions thrown because of JSON decoding errors.
    """
    explanation = 'The server failed to decode the JSON data included with ' \
                  'the request.'


class APIValidationError(APIBadRequest):
    """
    Subclass of :class:`~APIBadReqeust` used to set a custom explanation for
    :class:`marshmallow.ValidationError` and
    :class:`mongoengine.ValidationError` exceptions.
    """
    explanation = 'The server could not comply with the request because it ' \
                  'contains invalid data.'


class APIForbidden(httpexceptions.HTTPForbidden):
    """
    Subclass of :class:`~HTTPUnauthorized` used to raise HTTP exceptions within
    the API instead of forwarding the user to a front-end styled exception
    page.

    code: 403, title: Forbidden
    """


class APIAuthenticationFailed(APIForbidden):
    """
    Subclass of :class:`~APIForbidden` used to set a custom explanation for
    :class:`stackcite.data.AuthenticationError`.
    """
    explanation = 'Authentication failed.'


class APINotFound(httpexceptions.HTTPNotFound):
    """
    Subclass of :class:`~HTTPNotFound` used to raise HTTP exceptions within
    the API instead of forwarding the user to a front-end styled exception
    page.

    code: 404, title: Not Found
    """


class APIConflict(httpexceptions.HTTPConflict):
    """
    Subclass of :class:`~HTTPConflict` used to raise HTTP exceptions within
    the API instead of forwarding the user to a front-end styled exception
    page.

    code: 409, title: Conflict
    """


class APINotUniqueError(APIConflict):
    """
    Subclass of :class:`~APIConflict` used to set a custom explanation for
    :class:`mongoengine.NotUniqueError` exceptions.
    """
    explanation = 'The server could not comply with the request because it ' \
                  'contains insufficiently unique data.'


class APIInternalServerError(httpexceptions.HTTPInternalServerError):
    """
    Subclass of :class:`~HTTPInternalServerError` used to raise HTTP exceptions
    within the API instead of forwarding the user to a front-end styled
    exception page.

    code: 500, title: Internal Server Error
    """
