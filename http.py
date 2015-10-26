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
        re = re.match('^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?', url)
        scheme   = re.group(2)
        hostpart = re.group(4)   # user:pass@host:port
        uri      = re.group(5)
        query    = re.group(7)
        fragment = re.group(9)



    def do_request(self, url, payload=False, type="GET"):
        # explode url into: protocol, host, port, uri (maybe GET parameters), hash
        pass
