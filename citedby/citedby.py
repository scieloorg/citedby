# encode: utf-8

import urlparse
import argparse
import json

import pymongo
import utils
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response

from controller import query_by_pid, query_by_doi

@view_config(route_name='index', request_method='GET')
def index(request):
    return Response('Cited by SciELO API')

@view_config(route_name='citedby_pid', request_method='GET', renderer='json')
def citedby_pid(request):
    if not 'q' in request.GET:
        return None
    
    articles = query_by_pid(request.db['articles'], request.GET['q'])

    return articles


@view_config(route_name='citedby_doi', request_method='GET', renderer='json')
def citedby_doi(request):
    if not 'q' in request.GET:
        return None
    
    articles = query_by_doi(request.db['articles'], request.GET['q'])

    return articles

@view_config(route_name='citedby_meta', request_method='GET', renderer='json')
def citedby_meta(request):
    if not 'title' in request.GET or not 'author' in request.GET or not 'year' in request.GET:
        return None
    
    articles = query_by_meta(request.db['articles'],
        title=request.GET['title'],
        author=request.GET['author'],
        year=request.GET['year'])

    return articles

def main(settings, *args, **xargs):
    config_citedby = Configurator(settings=settings)

    db_url = urlparse.urlparse(settings['app']['mongo_uri'])

    config_citedby.registry.db = pymongo.Connection(host=db_url.hostname, port=db_url.port)

    def add_db(request):
        db = config_citedby.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db

    config_citedby.add_route('index', '/')
    config_citedby.add_route('citedby_pid', '/api/v1/pid/')
    config_citedby.add_route('citedby_doi', '/api/v1/doi/')
    config_citedby.add_request_method(add_db, 'db', reify=True)
    config_citedby.scan()

    return config_citedby.make_wsgi_app()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='API Cited By SciELO.')
    parser.add_argument('--config_file', '-c', type=str, default='../config.ini')

    args = parser.parse_args()
    config = utils.Configuration.from_file(args.config_file)

    settings = dict(config.items())

    app = main(settings)

    server = make_server(settings['http_server']['ip'], int(settings['http_server']['port']), app)

    server.serve_forever()