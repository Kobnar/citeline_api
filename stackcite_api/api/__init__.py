from pyramid import httpexceptions as _http_exc

from . import resources, schemas, views
from . import auth
from . import citations
from . import organizations
from . import people
from . import sources
from . import users


VERSIONS = ('v0',)
VERSION = VERSIONS[-1]


def root_redirect(context, request):
    return _http_exc.HTTPFound('/{}/'.format(VERSION))


def traversal_factory(parent, name):
    # Index
    parent[name] = resources.APIIndex
    api_idx = parent[name]
    # Collections
    auth.traversal_factory(api_idx, 'auth')
    people.traversal_factory(api_idx, 'people')
    organizations.traversal_factory(api_idx, 'organizations')
    sources.traversal_factory(api_idx, 'sources')
    citations.traversal_factory(api_idx, 'citations')
    users.traversal_factory(api_idx, 'users')
    return parent


def _endpoint_factory(config, endpoints):
    """
    Configures a REST endpoint for a collection/document pair of resources.

    NOTE: Resource ACL permissions must match view class attribute!

    :param config: A Pyramid configuration object
    :param endpoints: A two-tuple containing a collection and document resource
    """
    for resource in endpoints:
        view_class = resource.VIEW_CLASS
        for method, attr in view_class.METHODS:
            config.add_view(
                view_class,
                context=resource,
                request_method=method,
                attr=attr,
                permission=attr
            )


def view_factory(config):
    """
    Configures API endpoint views for an explicitly defined collection of
    resources.
    """

    config.add_view(
        views.APIIndexViews, context=resources.APIIndex, attr='index')

    _endpoint_factory(config, auth.ENDPOINTS)
    _endpoint_factory(config, people.ENDPOINTS)
    _endpoint_factory(config, organizations.ENDPOINTS)
    _endpoint_factory(config, sources.ENDPOINTS)
    _endpoint_factory(config, citations.ENDPOINTS)
    _endpoint_factory(config, users.ENDPOINTS)
