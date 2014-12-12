from icitation import ICitation

from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    def add_index(request):
        return ICitation()

    config.add_route('index', '/')
    config.add_route('citedby_pid', '/api/v1/pid/')
    config.add_route('citedby_doi', '/api/v1/doi/')
    config.add_route('citedby_meta', '/api/v1/meta/')
    config.add_request_method(add_index, 'index', reify=True)
    config.scan()

    return config.make_wsgi_app()
