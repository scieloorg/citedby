import urlparse
import argparse
import json

import pymongo
import utils
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response


@view_config(route_name='index', request_method='GET')
def index(request):
    return Response('Cited by SciELO API')

@view_config(route_name='citedby_pid', request_method='GET')
def citedby_pid(request):
    sn = request.db['articles'].find_one({'code': request.matchdict['pid']}, {'article': 1})

    del(sn['_id'])

    return Response(json.dumps(sn))


@view_config(route_name='citedby_doi', request_method='GET')
def citedby_doi(request):
    sn = request.db['articles'].find_one({'code': request.matchdict['doi']},  {'article': 1})

    del(sn['_id'])

    return Response(json.dumps(sn))

@view_config(route_name='citedby_title', request_method='GET')
def citedby_title(request):
    sn = request.db['articles'].find_one({'code': request.matchdict['title']}, {'article': 1})

    del(sn['_id'])

    return Response(json.dumps(sn))


def main(config, *args, **xargs):
    settings = dict(config.items())
    config_citedby = Configurator(settings=settings)

    db_url = urlparse.urlparse(settings['app']['mongo_uri'])

    config_citedby.registry.db = pymongo.Connection(host=db_url.hostname, port=db_url.port)

    def add_db(request):
        db = config_citedby.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db

    config_citedby.add_route('index', '/')
    config_citedby.add_route('citedby_pid', '/api/v1/pid/{pid}/')
    config_citedby.add_route('citedby_doi', '/api/v1/doi/{doi}/')
    config_citedby.add_route('citedby_title', '/api/v1/title/{title}/')
    config_citedby.add_request_method(add_db, 'db', reify=True)
    config_citedby.scan()

    return config_citedby.make_wsgi_app()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='API Cited By SciELO.')
    parser.add_argument('--config_file', '-c', type=str, default='../config.ini')

    args = parser.parse_args()
    config = utils.Configuration.from_file(args.config_file)

    app = main(config)

    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()