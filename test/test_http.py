#!/usr/bin/env micropython

import sys
import unittest

sys.path.insert(0, '..')

class TestHttp(unittest.TestCase):
    def setUp(self):
        import http
        self.http = http.HTTP()

    def test_parse_url(self):
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


if __name__ == '__main__':
    unittest.main()
