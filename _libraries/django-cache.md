
Cache Framework

backend:
memcached,database,filesystem, local-memory etc

per-site cache
per-view cache
template fragment cache
low-level cache API:(prefix, version, transformlation, etc)


Downstream caches

ISP
proxy cache: squid,
browser

譬如把/emails/inbox cache的话，但是不同人应该看到不同的，所以结合vary 头部一起

A number of HTTP headers exist to instruct downstream caches to differ their cache contents depending on designated variables, and to tell caching mechanisms not to cache particular pages. 

Django’s cache system creates its cache keys using the requested path and query – e.g., "/stories/2005/?order_by=author".



```python
@cache_page(60 * 15, cache="special_cache")
def my_view(request):
    pass

urlpatterns = ('',
    (r'^foo/(\d{1,2})/$', cache_page(60 * 15)(my_view)),
)

{% load cache %}
{% cache 500 sidebar request.user.username %}
    .. sidebar for logged in user ..
{% endcache %}

cache.set_many({'a': 1, 'b': 2, 'c': 3})
cache.set('my_key', 'hello, world!', 30)

@vary_on_headers('User-Agent', 'Cookie')
def my_view(request):
    # ...

@cache_control(must_revalidate=True, max_age=3600)
def my_view(request):
    # ...
```