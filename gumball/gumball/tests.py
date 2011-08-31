import unittest


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        from gumball.sample.application import main
        app = main()
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_site_layout(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue('site_layout' in res.body)

    def test_index(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue('testable' in res.body)

    @unittest.expectedFailure
    def test_static_jslibs(self):
        url = '/static-jslibs/jquery-1.6.2-jquery-ui-1.9m5.min.js'
        res = self.testapp.get(url, status=200)
        self.assertTrue('sizzle' in res.body)
