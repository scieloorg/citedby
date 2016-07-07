# coding: utf-8

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.settings import asbool, aslist


@view_config(route_name='index', request_method='GET')
def index(request):
    return Response('Cited by SciELO API')


@view_config(route_name='status', request_method='GET', renderer='jsonp')
def status(request):

    mems_addr = aslist(
        request.registry.settings.get('memcached_arguments_url', [])
    )

    response = {
        'health': {
            'is_alive_es_cluster': request.controller.get_status_cluster()
        }
    }

    return response


@view_config(route_name='citedby_pid', request_method='GET', renderer='jsonp')
def citedby_pid(request):

    if 'q' not in request.GET:
        raise HTTPBadRequest("parameter 'q' is required")

    if 'metaonly' in request.GET:
        if not request.GET.get('metaonly') in ['true', 'false']:
            raise HTTPBadRequest("parameter 'metaonly' must be 'true' or 'false'")

    metaonly = asbool(request.GET.get('metaonly'))

    articles = request.controller.query_by_pid(
        request.GET.get('q'),
        request.GET.get('collection', None),
        metaonly
    )

    return articles


@view_config(route_name='citedby_doi', request_method='GET', renderer='jsonp')
def citedby_doi(request):

    if 'q' not in request.GET:
        raise HTTPBadRequest("parameter 'q' is required")

    if 'metaonly' in request.GET:
        if not request.GET.get('metaonly') in ['true', 'false']:
            raise HTTPBadRequest("parameter 'metaonly' must be 'true' or 'false'")

    metaonly = asbool(request.GET.get('metaonly'))

    articles = request.controller.query_by_doi(request.GET.get('q'), metaonly)

    return articles


@view_config(route_name='citedby_meta', request_method='GET', renderer='jsonp')
def citedby_meta(request):

    if 'title' not in request.GET:
        raise HTTPBadRequest("at least the parameter 'title' is required")

    if 'metaonly' in request.GET:
        if not request.GET.get('metaonly') in ['true', 'false']:
            raise HTTPBadRequest("parameter 'metaonly' must be 'true' or 'false'")

    metaonly = asbool(request.GET.get('metaonly'))

    articles = request.controller.query_by_meta(
        request.GET.get('title', ''),
        request.GET.get('author', ''),
        request.GET.get('year', ''),
        metaonly
    )

    return articles
