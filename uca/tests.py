import unittest


class UCATests(unittest.TestCase):

    def test_validate_url(self):
        from lib.uca import validate_url
        from lib.uca import UrlValidate

        is_legal, msg = validate_url(None)
        self.failUnless(is_legal is False and msg == UrlValidate.EMPTY_URL)

        is_legal, msg = validate_url('www.google.com')
        self.failUnless(is_legal is False and msg == UrlValidate.EMPTY_PROTO)

        is_legal, msg = validate_url('ftp://www.google.com')
        self.failUnless(is_legal is False and msg == UrlValidate.INVALID_PROTO)

        is_legal, msg = validate_url('http://aa.b')
        self.failUnless(is_legal is False and msg == UrlValidate.URL_TOO_SHORT)

        is_legal, msg = validate_url('http://www.google-.com')
        self.failUnless(is_legal is False and msg == UrlValidate.INVALID_URL)

        is_legal, msg = validate_url('http://www.google.com?')
        self.failUnless(is_legal is False and msg == UrlValidate.INVALID_URL)

        is_legal, msg = validate_url('http://www.google.com/')
        self.failUnless(is_legal is True and msg == UrlValidate.SUCCESS)
