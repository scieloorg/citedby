# coding: utf-8

from pyramid.config import Configurator
from pyramid.renderers import JSONP
from pyramid.settings import aslist

from icontroller import cache_region


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.add_renderer('jsonp', JSONP(param_name='callback', indent=4))

    hosts = aslist(settings['elasticsearch_host'])

    cache_region.configure(
        'dogpile.cache.bmemcached',
        expiration_time=int(settings['memcached_expiration_time']),
        arguments={'url': aslist(settings['memcached_arguments_url'])})

    config.add_route('index', '/')
    config.add_route('stats', '/_stats/')
    config.add_route('citedby_pid', '/api/v1/pid/')
    config.add_route('citedby_doi', '/api/v1/doi/')
    config.add_route('citedby_meta', '/api/v1/meta/')
    config.scan()

    return config.make_wsgi_app()
