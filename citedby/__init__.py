import os
from pyramid.config import Configurator
from pyramid.renderers import JSONP
from pyramid.settings import aslist

from citedby import controller
from citedby.controller import cache_region as controller_cache_region


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.add_renderer('jsonp', JSONP(param_name='callback', indent=4))

    def add_controller(request):

        es = os.environ.get(
            'ELASTICSEARCH_HOST',
            settings.get('elasticsearch_host', '127.0.0.1:9200')
        )

        es_index = os.environ.get(
            'ELASTICSEARCH_INDEX',
            settings.get('elasticsearch_index', 'citations')
        )

        return controller.controller(
            aslist(es),
            sniff_on_connection_fail=True,
            timeout=600
        ).set_base_index(es_index)

    config.add_route('index', '/')
    config.add_route('status', '/_status/')
    config.add_route('citedby_pid', '/api/v1/pid/')
    config.add_route('citedby_doi', '/api/v1/doi/')
    config.add_route('citedby_meta', '/api/v1/meta/')
    config.add_request_method(add_controller, 'controller', reify=True)

    # Cache Settings Config
    memcached_host = os.environ.get(
        'MEMCACHED_HOST',
        settings.get('memcached_host', None)
    )

    memcached_expiration_time = os.environ.get(
        'MEMCACHED_EXPIRATION_TIME',
        settings.get('memcached_expiration_time', 2592000)  # a month cache
    )

    if 'memcached_host' is not None:
        cache_config = {}
        cache_config['expiration_time'] = int(memcached_expiration_time)
        cache_config['arguments'] = {'url': memcached_host, 'binary': True}
        controller_cache_region.configure('dogpile.cache.pylibmc', **cache_config)
    else:
        controller_cache_region.configure('dogpile.cache.null')

    config.scan()

    return config.make_wsgi_app()
