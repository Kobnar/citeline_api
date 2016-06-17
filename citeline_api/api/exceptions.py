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
