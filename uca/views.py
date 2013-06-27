from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from lib.uca import get_hash_value
from lib.uca import validate_url
from lib.uca import UrlValidate


@view_config(route_name='root', renderer='templates/root.jinja2', request_method='GET', http_cache=(86400))
def view_root(request):
    return {}


@view_config(route_name='api1', renderer='jsonp')
def api_1(request):
    url = request.GET.get('link')
    is_url_OK, msg = validate_url(url)
    if is_url_OK is False:
        return {'err': True, 'link': '', 'msg': msg}
    try:
        hashValue = get_hash_value(url)
    except ValueError:
        return {'err': True, 'link': '', 'msg': UrlValidate.UNKNOWN_ERROR}

    hashUrl = request.host_url + '/' + hashValue
    link_table = request.db['uca']
    result = link_table.find_one({'_id': hashValue})
    if result is None:
        link_table.insert({'_id': hashValue, 'l': url})
    return {'err': False, 'hashLink': hashUrl}


@view_config(route_name='redirect')
def view_redirect(request):
    link_table = request.db['uca']
    hash_value = request.matchdict['hash_value']
    result = link_table.find_one({'_id': hash_value})
    if result is None:
        return HTTPNotFound(u'The link not exists')
    else:
        return HTTPFound(location=result['l'])
