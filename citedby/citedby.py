# coding: utf-8

import json
import urlparse

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.settings import asbool, aslist
from pylibmc.test import make_test_client, NotAliveError

from icontroller import query_by_pid, query_by_doi, query_by_meta


@view_config(route_name='index', request_method='GET')
def index(request):
    return Response('Cited by SciELO API')


@view_config(route_name='stats', request_method='GET', renderer='jsonp')
def stats(request):
    memcacheds = {}

    mems_addr = aslist(
        request.registry.settings.get('memcached_arguments_url', None))

    for mem in mems_addr:

        addr, port = mem.split(':')

        try:
            alive = bool(make_test_client(host=addr, port=port))
            memcacheds[mem] = alive
        except NotAliveError:
            memcacheds[mem] = False

    return {'health': {'is_alive_es_cluster': request.index._ping(),
            'is_alive_memcached': memcacheds}}


@view_config(route_name='citedby_pid', request_method='GET', renderer='jsonp')
def citedby_pid(request):

    if 'q' not in request.GET:
        raise HTTPBadRequest("parameter 'q' is required")

    if 'metaonly' in request.GET:
        if not request.GET.get('metaonly') in ['true', 'false']:
            raise HTTPBadRequest("parameter 'metaonly' must be 'true' or 'false'")

    metaonly = asbool(request.GET.get('metaonly'))

    articles = query_by_pid(request.GET.get('q'), metaonly)

    return articles


@view_config(route_name='citedby_doi', request_method='GET', renderer='jsonp')
def citedby_doi(request):

    if 'q' not in request.GET:
        raise HTTPBadRequest("parameter 'q' is required")

    if 'metaonly' in request.GET:
        if not request.GET.get('metaonly') in ['true', 'false']:
            raise HTTPBadRequest("parameter 'metaonly' must be 'true' or 'false'")

    metaonly = asbool(request.GET.get('metaonly'))

    articles = query_by_doi(request.GET.get('q'), metaonly)

    return articles


@view_config(route_name='citedby_meta', request_method='GET', renderer='jsonp')
def citedby_meta(request):

    if 'title' not in request.GET:
        raise HTTPBadRequest("at least the parameter 'title' is required")

    if 'metaonly' in request.GET:
        if not request.GET.get('metaonly') in ['true', 'false']:
            raise HTTPBadRequest("parameter 'metaonly' must be 'true' or 'false'")

    metaonly = asbool(request.GET.get('metaonly'))

    articles = query_by_meta(request.GET.get('title', ''),
                             request.GET.get('author', ''),
                             request.GET.get('year', ''),
                             metaonly)
    return articles
