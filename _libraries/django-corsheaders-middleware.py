
# django-cors-headers


### usage

在CommonMiddleware会把一些请求304回去（并且不再走后续的middleware等流程）
Note that CorsMiddleware needs to come before Django's CommonMiddleware if you are using Django's USE_ETAGS = True setting,
otherwise the CORS headers will be lost from the 304 not-modified responses, causing errors in some browsers.


CORS_ORIGIN_REGEX_WHITELIST = ('^http?://(\w+\.)?google\.com$', )
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_CREDENTIALS = True

# corsheaders.defaults

from django.conf import settings

default_headers = (
	'x-requested-with',
	'content-type',
	'accept',
	'origin',
	'authorization',
	'x-crsftoken',
)

CORS_ALLOW_HEADERS = getattr(settings, 'CORS_ALLOW_HEADERS', default_headers)

# also for default_methods

CORS_ORIGIN_REGEX_WHITELIST = getattr(settings, 'CORS_ORIGIN_REGEX_WHITELIST', ())
CORS_URLS_REGEX = getattr(settings, 'CORS_URLS_REGEX', '^.*$')

CORS_ORIGIN_WHITELIST = getattr(settings, 'CORS_ORIGIN_WHITELIST', ())
CORS_ORIGIN_ALLOW_ALL = getattr(settings, 'CORS_ORIGIN_ALLOW_ALL', False)


# corsheaders.middleware

class CorsMiddleware(object):

	def process_request(self, request):
		# If CORS preflight header, then create an empty body response (200 OK) and return it
		if (self.is_enabled(request) and
			request.method == 'OPTIONS' and
			'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META):
			response = http.HttpResponse()
			return response
		return None

	def process_response(self, request, response):
		origin = request.META.get('HTTP_ORIGIN')
		if self.is_enabled(request) and origin:
			url = urlparse(origin)

			if not settings.CORS_ORIGIN_ALLOW_ALL and self.origin_not_found_in_white_lists(origin, url):
				return response

			response[ACCESS_CONTROL_ALLOW_ORIGIN] = '*' if settings.CORS_ORIGIN_ALLOW_ALL

			if settings.CORS_ALLOW_CREDENTIALS:
				response[ACCESS_CONTROL_ALLOW_CREDENTIALS] = 'true'

			if request.method == 'OPTIONS':
				# ADD allow_headers, allow_methods, even max_age

		return response

	def regex_domain_match(self, origin):
		for domain_pattern in settings.CORS_ORIGIN_REGEX_WHITELIST:
			if re.match(domain_pattern, origin):
				return origin

	def is_enabled(self, request):
		return re.match(settings.CORS_URLS_REGEX, request.path)