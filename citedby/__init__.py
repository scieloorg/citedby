from pyramid.renderers import JSONP
from pyramid.config import Configurator
from pyramid.settings import aslist, asbool

from icitation import ICitation
from citedby import cache_region


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.add_renderer('jsonp', JSONP(param_name='callback', indent=4))

    hosts = aslist(settings['elasticsearch_host'])

    def add_index(request):
        return ICitation(hosts=hosts, sniff_on_start=True,
                         sniff_on_connection_fail=True)

    cache_region.configure('dogpile.cache.pylibmc',
            expiration_time=int(settings['memcached_expiration_time']),
            arguments= {
                        'url': aslist(settings['memcached_arguments_url']),
                        'binary': asbool(settings['memcached_binary']),
                        'behaviors':{"tcp_nodelay": True,
                                     "ketama":True,
                                     "remove_failed": 2,
                                     "dead_timeout": 10,
                                     "num_replicas": 2}
                        },
            _config_prefix=settings['memcached_prefix'])

    config.add_route('index', '/')
    config.add_route('stats', '/_stats/')
    config.add_route('citedby_pid', '/api/v1/pid/')
    config.add_route('citedby_doi', '/api/v1/doi/')
    config.add_route('citedby_meta', '/api/v1/meta/')
    config.add_request_method(add_index, 'index', reify=True)
    config.scan()

    return config.make_wsgi_app()
