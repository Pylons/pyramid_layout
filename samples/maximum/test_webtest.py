from unittest import TestCase
from webtest import TestApp

class BottlecapFunctionalTests(TestCase):
    def setUp(self):
        from application import main
        app = main()
        self.testapp = TestApp(app)

    def test_it(self):
        res = self.testapp.get('/', status=200)
        self.failUnless('Some' in res.body)