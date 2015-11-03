#!/usr/bin/env micropython

import sys
import unittest

sys.path.insert(0, '..')

class TestHttp(unittest.TestCase):
    def setUp(self):
        import http
        self.http = http.HTTP()

    def test_parse_url1(self):
        urlparts = self.http.parse_url('https://user:passwd@example.org:1234/test?x=3&y=4#fragme')
        self.assertEqual(urlparts.scheme, 'https')
        self.assertEqual(urlparts.hostname, 'example.org')
        self.assertEqual(urlparts.path, '/test')
        self.assertEqual(urlparts.query, 'x=3&y=4')
        self.assertEqual(urlparts.fragment, 'fragme')
        self.assertEqual(urlparts.username, 'user')
        self.assertEqual(urlparts.password, 'passwd')
        self.assertEqual(urlparts.port, 1234)

    def test_parse_url2(self):
        urlparts = self.http.parse_url('http://example.org/test')
        self.assertEqual(urlparts.scheme, 'http')
        self.assertEqual(urlparts.hostname, 'example.org')
        self.assertEqual(urlparts.path, '/test')
        self.assertEqual(urlparts.query, '')
        self.assertEqual(urlparts.fragment, '')
        self.assertEqual(urlparts.username, None)
        self.assertEqual(urlparts.password, None)
        self.assertEqual(urlparts.port, None)

    def test_parse_url3(self):
        urlparts = self.http.parse_url('http://user@example.org/test')
        self.assertEqual(urlparts.scheme, 'http')
        self.assertEqual(urlparts.hostname, 'example.org')
        self.assertEqual(urlparts.path, '/test')
        self.assertEqual(urlparts.query, '')
        self.assertEqual(urlparts.fragment, '')
        self.assertEqual(urlparts.username, 'user')
        self.assertEqual(urlparts.password, None)
        self.assertEqual(urlparts.port, None)

    def test_parse_url4(self):
        urlparts = self.http.parse_url('http://example.org:1234/test')
        self.assertEqual(urlparts.scheme, 'http')
        self.assertEqual(urlparts.hostname, 'example.org')
        self.assertEqual(urlparts.path, '/test')
        self.assertEqual(urlparts.query, '')
        self.assertEqual(urlparts.fragment, '')
        self.assertEqual(urlparts.username, None)
        self.assertEqual(urlparts.password, None)
        self.assertEqual(urlparts.port, 1234)

    def test_parse_ipv6_1(self):
        urlparts = self.http.parse_url('http://[fedc:ba98::3210]/test')
        self.assertEqual(urlparts.hostname, '[fedc:ba98::3210]')

    def test_parse_ipv6_2(self):
        urlparts = self.http.parse_url('http://[fedc:ba98::3210]:1234/test')
        self.assertEqual(urlparts.hostname, '[fedc:ba98::3210]')
        self.assertEqual(urlparts.port, 1234)

    def test_parse_ipv6_3(self):
        urlparts = self.http.parse_url('http://[::FFFF:129.144.52.38]:5678/blah')
        self.assertEqual(urlparts.hostname, '[::FFFF:129.144.52.38]')
        self.assertEqual(urlparts.port, 5678)

if __name__ == '__main__':
    unittest.main()
