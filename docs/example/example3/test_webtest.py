from unittest import TestCase
from webtest import TestApp

class BottlecapFunctionalTests(TestCase):
    def setUp(self):
        from example import main
        app = main({})
        self.testapp = TestApp(app)

    def test_it(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue('Hello World, In Popper' in res.body)
        self.assertTrue('Item 1' not in res.body)
        self.assertTrue('Projects' in res.body)
        self.assertTrue('Customers' in res.body)

