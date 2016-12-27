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


class APINotFound(httpexceptions.HTTPNotFound):
    """
    Subclass of :class:`~HTTPNotFound` used to raise HTTP exceptions within
    the API instead of forwarding the user to a front-end styled exception
    page.

    code: 404, title: Not Found
    """


class APIUnauthorized(httpexceptions.HTTPUnauthorized):
    """
    Subclass of :class:`~HTTPUnauthorized` used to raise HTTP exceptions within
    the API instead of forwarding the user to a front-end styled exception
    page.

    code: 401, title: Unauthorized
    """


class APIForbidden(httpexceptions.HTTPForbidden):
    """
    Subclass of :class:`~HTTPUnauthorized` used to raise HTTP exceptions within
    the API instead of forwarding the user to a front-end styled exception
    page.

    code: 403, title: Forbidden
    """


class APIConflict(httpexceptions.HTTPConflict):
    """
    Subclass of :class:`~HTTPConflict` used to raise HTTP exceptions within
    the API instead of forwarding the user to a front-end styled exception
    page.

    code: 409, title: Conflict
    """
