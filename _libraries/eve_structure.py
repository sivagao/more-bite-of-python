

DOMAIN = {
    'contacts': contacts,
    'invoices': invoices
}

invoices = {
    'item_lookup': False,
    'schema': {},
}

contacts = {
    'url': 'contatti',
    'cache_control': 'max-age=20, must-revalidate',
    'cache_expires': 20,
    'item_title': 'contatto',
    'additional_lookup': {},
    'schema': {}
}


from endpoints import collections_endpoint, item_endpoint, home_endpoint
class Eve(Flaks):

    def __init__(self, *args, **kwargs):
        pass

    def load_config(self):
        self.config.from_object(eve)

        try:
            self.config.from_pyfile()
            self.config.from_envvar('EVE_SETTINGS')
        except:
            pass

    def validate_config(self):
        pass

    def set_defaults(self):
        pass

    def add_url_rules(self):

        for resource, setting in self.config['DOMAIN'].items():


            self.add_url_rule(url, view_func=collections_endpoint, method=settings['methods'])

            if settings['item_lookup'] is True:
                pass

            add_lookup = settings.get('additional_lookup')
            if add_lookup:
                pass

        self.config['RESOURCES'] = resources
        self.config['URLS'] = urls

# endpoints
from methods import get, getitem, post, patch, delte
from flask import request
from render import send_response

def collections_endpoint(url):
    resource = config.RESOURCES[url]
    response = None
    if request.method == 'GET':
        response = get(response)
    elif request.method == 'POST':
        response = post(response)
    elif request.method == 'DELETE':
        pass

    if response:
        return send_response(resource, *response)

def item_endpoint(url, **lookup):
    pass

def home_endpoint():
    response = dict()
    links = list()
    for resource in config.DOMAIN.keys():
        links.append("<link rel='child' title='%s' href='%s' >" % (config.URLS[resource], collection_link(resource)))
    response['links'] = links
    return send_response(None, response)


# methods/get.py
from flask import current_app as app
from eve.utils import parse_request, document_etag, document_link, \
    collection_link, home_link, querydef, resource_uri

def get(resource):
    documents = list()
    response = dict()
    last_updated = datetime.min

    req = parse_request()
    cursor = app.data.find(resource, req)
    for index, document in enumerate(cursor):
        if document[LAST_UPDATED] > last_updated:
            last_updated = document[LAST_UPDATED]
        document['etag'] = document_etag(document)
        document['link'] = document_link(resource, document[ID_FIELD])

        documents.append(document)
    if request.if_modified_since and len(documents) == 0:
        status = 304
        last_modified = None
    else:
        status = 200
        last_modified = last_updated lf last_updated > datetime.min else None
        response[resource] = documents
        response['links'] = paging_links(resource, req, index)
    etag = None
    return response, last_modified, etag, status

def paging_links(resource, req, documents_count):
    paging_links = standard_links(resource)

    if documents_count:
        if req.page * req.max_results < documents_count:
            q = querydef(req,.max_results, req.where, req.sort, page+1)
            paging_links.append("<link rel='next' title='next page'>"
                                " href='%s%s' />" % (resource_uri(resource), q))
        if req.page > 1:
            q = querydef(req.max_results, req.where, req.sort, req.page -1)
            paging_links.append("<link rel='prev' title='previous page'>"
                                " href='%s%s' />" % (resource_uri(resource), q))

    return paging_links

def standard_links(resource):
    return [home_link(), collection_link(resource)]

# utils.py
class ParsedRequest:
    def __init__():
        pass

def parse_request():
    pass

def querydef(max_results=config.PAGING_DEFAULT, where=None, sort=None, page=None):
    pass

def resource_uri(resource):
    return "%s/%s" % (config.BASE_URI, config.URLS[resource])

# io/base.py
class DataLayer:
    def __init__():
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        raise NotImplementedError

    def find(self, resource, where=None, sort=None, page=1, max_results=config.PAGING_DEFAULT, if_modified_since=None):
        raise NotImplementedError

    def find_one(self, resource, document):
        raise NotImplementedError

    def update():
        pass

    def remove():
        pass

class Mongo(DataLayer):
    def init_app(self, app):
        self.driver = PyMongo(app)

    def find(self, resource, req):
        args = dict()

        args['limit'] = req.max_results

        if req.page > 1:
            args['skip'] = (req.page -1) * req.max_results

        if req.sort:
            args['sort'] = ast.literal_eval(req.sort)

        spec = dict()
        if req.where:
            spec = json.loads(req.where)

        if req.if_modified_since:
            spec[config.LAST_UPDATED] = {'$gt': req.if_modified_since}

        if len(spec) > 0:
            args['spec'] = spec

        cursor = self.driver.db[resource].find(**args)
        for document in cursor:
            self.fix_last_updated(document)
            yield document

    def find_one(self, resource, **lookup):
        try:
            if config.ID_FIELD in lookup:
                lookup[ID_FIELD] = OjectId(lookup[ID_FIELD])
        except:
            pass
        document = self.driver.db[resource].find_one(lookup)
        if document:
            self.fix_last_updated(document)
        return document

