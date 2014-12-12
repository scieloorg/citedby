# encode: utf-8

import urlparse
import json

from pyramid.view import view_config, notfound_view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from icontroller import query_by_pid, query_by_doi, query_by_meta


@notfound_view_config(append_slash=True)
def notfound(request):
    return HTTPNotFound('Not found')


@view_config(route_name='index', request_method='GET')
def index(request):
    return Response('Cited by SciELO API')


@view_config(route_name='citedby_pid', request_method='GET', renderer='json')
def citedby_pid(request):
    if not 'q' in request.GET:
        return None

    articles = query_by_pid(request.index, request.GET['q'])

    return articles


@view_config(route_name='citedby_doi', request_method='GET', renderer='json')
def citedby_doi(request):
    if not 'q' in request.GET:
        return None

    articles = query_by_doi(request.index, request.GET['q'])

    return articles


@view_config(route_name='citedby_meta', request_method='GET', renderer='json')
def citedby_meta(request):
    if not 'title' in request.GET:
        return None

    articles = query_by_meta(
        request.index,
        title=request.GET.get('title', ''),
        author_surname=request.GET.get('author', ''),
        year=request.GET.get('year', '')
    )

    return articles
