from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response

@view_config(route_name='index', request_method='GET')
def index(request):
    return Response('Cited by SciELO API')

@view_config(route_name='citedby_pid', request_method='GET')
def citedby_pid(request):
    return Response('This is the cited by SciELO service, for a given PID')

@view_config(route_name='citedby_doi', request_method='GET')
def citedby_doi(request):
    return Response('This is the cited by SciELO service, for a given DOI')

@view_config(route_name='citedby_title', request_method='GET')
def citedby_title(request):
    return Response('This is the cited by SciELO service, for a given article title')

if __name__ == '__main__':
    config = Configurator()
    config.add_route('index', '/')
    config.add_route('citedby_pid', '/api/v1/pid')
    config.add_route('citedby_doi', '/api/v1/doi')
    config.add_route('citedby_title', '/api/v1/title')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
