"""
Test Route
# route with relative path
>>> Route('web', BaseHandler())({'REL_REQUEST_URI': '/web/test.example.com', 'SCRIPT_NAME': ''}, False)
{'wb_url': ('latest_replay', '', '', 'http://test.example.com', 'http://test.example.com'), 'coll': 'web', 'wb_prefix': '/web/', 'request_uri': '/web/test.example.com'}

# route with absolute path, running at script /my_pywb
>>> Route('web', BaseHandler())({'REL_REQUEST_URI': '/web/2013im_/test.example.com', 'SCRIPT_NAME': '/my_pywb', 'HTTP_HOST': 'localhost:8081', 'wsgi.url_scheme': 'https'}, True)
{'wb_url': ('replay', '2013', 'im_', 'http://test.example.com', '2013im_/http://test.example.com'), 'coll': 'web', 'wb_prefix': 'https://localhost:8081/my_pywb/web/', 'request_uri': '/web/2013im_/test.example.com'}


# not matching route -- skipped
>>> Route('web', BaseHandler())({'REL_REQUEST_URI': '/other/test.example.com', 'SCRIPT_NAME': ''}, False)


# Referer Redirect Test
>>> ReferRedirect('http://localhost:8080/').match_prefixs
['http://localhost:8080/']

>>> ReferRedirect(['http://example:9090/']).match_prefixs
['http://example:9090/']

>>> _test_redir('http://localhost:8080/', '/diff_path/other.html', 'http://localhost:8080/coll/20131010/http://example.com/path/page.html')
'http://localhost:8080/coll/20131010/http://example.com/diff_path/other.html'

>>> _test_redir('http://localhost:8080/', '/../other.html', 'http://localhost:8080/coll/20131010/http://example.com/path/page.html')
'http://localhost:8080/coll/20131010/http://example.com/other.html'

>>> _test_redir('http://localhost:8080/', '/../../other.html', 'http://localhost:8080/coll/20131010/http://example.com/index.html')
'http://localhost:8080/coll/20131010/http://example.com/other.html'

# Custom collection
>>> _test_redir('http://localhost:8080/', '/other.html', 'http://localhost:8080/complex/123/20131010/http://example.com/path/page.html', coll='complex/123')
'http://localhost:8080/complex/123/20131010/http://example.com/other.html'

# With timestamp included
>>> _test_redir('http://localhost:8080/', '/20131010/other.html', 'http://localhost:8080/coll/20131010/http://example.com/index.html')
'http://localhost:8080/coll/20131010/http://example.com/other.html'

# With timestamp included
>>> _test_redir('http://localhost:8080/', '/20131010/path/other.html', 'http://localhost:8080/coll/20131010/http://example.com/some/index.html')
'http://localhost:8080/coll/20131010/http://example.com/path/other.html'

# Wrong Host
>>> _test_redir('http://example:8080/', '/other.html', 'http://localhost:8080/coll/20131010/http://example.com/path/page.html')
False

# Right Host
>>> _test_redir('http://localhost:8080/', '/other.html', 'http://example.com:8080/coll/20131010/http://example.com/path/page.html', http_host = 'example.com:8080')
'http://example.com:8080/coll/20131010/http://example.com/other.html'

# With custom SCRIPT_NAME
>>> _test_redir('http://localhost:8080/', '/../other.html', 'http://localhost:8080/extra/coll/20131010/http://example.com/path/page.html', '/extra')
'http://localhost:8080/extra/coll/20131010/http://example.com/other.html'

# With custom SCRIPT_NAME + timestamp
>>> _test_redir('http://localhost:8080/', '/20131010/other.html', 'http://localhost:8080/extra/coll/20131010/http://example.com/path/page.html', '/extra')
'http://localhost:8080/extra/coll/20131010/http://example.com/other.html'

# With custom SCRIPT_NAME, bad match
>>> _test_redir('http://localhost:8080/', '/../other.html', 'http://localhost:8080/extra/coll/20131010/http://example.com/path/page.html', '/extr')
False


"""

from pywb.archivalrouter import Route, ReferRedirect
from pywb.handlers import BaseHandler


def _test_redir(match_host, request_uri, referrer, script_name = '', coll = 'coll', http_host = None):
    env = {'REL_REQUEST_URI': request_uri, 'HTTP_REFERER': referrer, 'SCRIPT_NAME': script_name}

    if http_host:
        env['HTTP_HOST'] = http_host

    routes = [Route(coll, BaseHandler())]

    redir = ReferRedirect(match_host)
    #req = WbRequest.from_uri(request_uri, env)
    rep = redir(env, routes)
    if not rep:
        return False

    return rep.status_headers.get_header('Location')


