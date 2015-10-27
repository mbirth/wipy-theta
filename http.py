"""
HTTP helper class
@author Markus Birth <markus@birth-online.de>

RFC: http://www.w3.org/Protocols/rfc2616/rfc2616.html
Inspiration: http://www.wellho.net/resources/ex.php4?item=y303/browser.py
"""
import re
import socket

class HTTP:
    def parse_url(self, url):
        # Taken from: https://tools.ietf.org/html/rfc3986#appendix-B
        re1 = re.match('^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?', url)
        scheme   = re1.group(2)
        hostpart = re1.group(4)   # user:pass@host:port
        uri      = re1.group(5)
        query    = re1.group(7)
        fragment = re1.group(9)

        # TODO: Not IPv6 ready!!!
        re2 = re.match('^(([^:]+)(:([^@]*))?@)?([^:]+)(:(\d+))?$', hostpart)
        #for i in range(0, 10):
        #    print(str(i) + ': ' + re2.group(i))

        username = re2.group(2) or None
        password = re2.group(4) or None
        hostname = re2.group(5) or None
        port     = re2.group(7) or None
        if port:
            port = int(port)

        return ParseResult(scheme, hostpart, uri, None, query, fragment, username, password, hostname, port)

    def do_request(self, url, payload=False, type="GET"):
        urlparts = self.parse_url(url)
        
        pass

class ParseResult():
    def __init__(self, scheme, netloc, path, params, query, fragment, username, password, hostname, port):
        self.scheme = scheme
        self.netloc = netloc
        self.path   = path
        self.params = params
        self.query  = query
        self.fragment = fragment
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port     = port
