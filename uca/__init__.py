import os

from pyramid.config import Configurator
from pyramid.renderers import JSONP

from urlparse import urlparse
from gridfs import GridFS
import pymongo


def add_mongo_db(request):
    settings = request.registry.settings
    db_url = settings['db_url']
    db = settings['db_conn'][db_url.path[1:]]
    if db_url.username and db_url.password:
        db.authenticate(db_url.username, db_url.password)
    request.db = db
    request.fs = GridFS(db)


def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    if os.environ.get('OPENSHIFT_MONGODB_DB_URL'):
    # OpenShift Settings
        settings['mongo_uri'] = \
            '%(OPENSHIFT_MONGODB_DB_URL)s%(OPENSHIFT_APP_NAME)s' % os.environ

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'uca:static/dist')
    config.add_route('root', '')
    config.add_route('api1', '/api/1/')
    config.add_renderer('jsonp', JSONP(param_name='callback'))
    config.add_route('redirect', '/{hash_value}')

    db_url = urlparse(settings['mongo_uri'])
    conn = pymongo.Connection(host=db_url.hostname,
                              port=db_url.port)
    config.registry.settings['db_conn'] = conn
    config.registry.settings['db_url'] = db_url
    config.add_request_method(add_mongo_db, 'db', reify=True)

    if settings['dev'] == 'true':
        def add_global(event):
            event['dev'] = True
        config.add_subscriber(add_global, 'pyramid.events.BeforeRender')

    config.scan()

    return config.make_wsgi_app()
