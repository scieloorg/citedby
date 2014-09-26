import urlparse

from pyramid.config import Configurator
import pymongo

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    db_url = urlparse.urlparse(settings['mongo_uri'])
    
    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db
    
    config.registry.db = pymongo.Connection(host=db_url.hostname, port=db_url.port)
    config.add_route('index', '/')
    config.add_route('citedby_pid', '/api/v1/pid/')
    config.add_route('citedby_doi', '/api/v1/doi/')
    config.add_route('citedby_meta', '/api/v1/meta/')
    config.add_request_method(add_db, 'db', reify=True)
    config.scan()

    return config.make_wsgi_app()