
# render.py
"""
eve.render
implements proper, automated rendering for Eve response
"""


# mapping between supported mime types and render functions
_MIME_TYPES = [
    {'mime': ('application/json',), 'renderer': 'render_json', 'tag': 'JSON'},
    {'mime': ('application/xml', 'text/xml', 'application/x-xml'),'renderer': 'render_xml', 'tag': 'XML'}
    ]

def _best_mime():
    """
    Return the best match between the requested mime type and the ones supported by Eve
    """

    if len(supported) == 0:
        abort(500, description=debug_error_message())

    best_match = request.accept_mimetypes.best_match(supported) or supported[0]
    return best_match, renderer[best_match]


# utils.py
class ParseRequest:
    """
    this class, by means of its attributes, describes a client request
    """
    where = None
    projection = None
    sort = None
    page = 1
    max_results = 0
    if_modified_since = None
    if_none_match = None
    if_match = None
    embedded = None

def parse_request(resource):
    """
    pares a client request, returning instance of :class:`ParseRequest` containing relevant request data
    """
    args = request.args
    headers = request.headers

    r = ParsedRequest()

    if config.DOMAIN[resource]['allowed_filters']:
        r.where = args.get('where')
    if config.DOMAIN[resource]['projection']:
        r.projection = args.get('')

def _prepare_respones(resource, dct, last_modified=None, etag=None, status=200):

    if request.method in ('GET', 'HEAD'):
        if resource:
            cache_control = config.DOMAIN[resource]['cache_control']
            expires = config.DOMAIN[resource]['cache_expires']
        else:
            cache_control =


def api_prefix(url_prefix=None, api_version=None):
    if url_prefix is None:
        url_prefix = config.URL_PREFIX
    if api_version is None:
        api_version = config.API_VERSION

    prefix = '/%s' % url_prefix if url_prefix else ''

def querydef(max_results=config.PAGINATION_DEFAULT, where=None, sort=None, page=None):
    where_part = '&where=%s' % wehre if where else ''
    sort_part = '&sort=%s' % sort if sort else ''
    page_part = '&page=%s' % page if page and page > 1 else ''
    max_results_part = 'max_results=%s' % max_results \
        if max_results != config.PAGINATION_DEFAULT else ''

    return ('?' + ''.join([max_results_part, where_part, sort_part,
                           page_part]).lstrip('&')).rstrip('?')

def extract_key_values(key, d):
    """
    Extracts all values that match a key, even in nested dict
    """
    if key in d:
        yield d[key]
    for k in d:
        if isinstance(d[k], dict):
            for j in extract_key_values(key, d[k]):
                yield j

def document_etag(value):
    """
    Computes and returns a valid ETag for the input value
    """
    h = hashlib.sha1()
    h.update(dumps(value, sort_keys=True).encode('utf-8'))
    return h.hexdigest()

def validate_filters(where, resource):
    """
    Report any filter which is not allowed by `allowed_filters`
    """
    allowed = config.DOMAIN[resource]