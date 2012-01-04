from unittest import TestCase
from webtest import TestApp

class BottlecapFunctionalTests(TestCase):
    def setUp(self):
        from samples.maximum.application import main
        app = main()
        self.testapp = TestApp(app)

    def test_it(self):
        # No need for longer tests by putting each view in its
        # own test. Run them all here.

        res = self.testapp.get('/', status=200)
        self.failUnless('Some' in res.body)

        # Default "tab" in People section
        res = self.testapp.get('/peopleosf', status=200)
        self.failUnless('Some' in res.body)

        # A report in that tab
        res = self.testapp.get('/peopleosfbaltimore', status=200)
        self.failUnless('Some' in res.body)

        # The /communities screen
        res = self.testapp.get('/communities', status=200)
        self.failUnless('Some' in res.body)

        # The blog in a community
        res = self.testapp.get('/communitiesblog', status=200)
        self.failUnless('Some' in res.body)

        # The test on the alternative layout, make sure it works
        res = self.testapp.get('/test', status=200)
        self.failUnless('Some' in res.body)
