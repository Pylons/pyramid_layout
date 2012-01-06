from unittest import TestCase
from webtest import TestApp

class BottlecapFunctionalTests(TestCase):
    def setUp(self):
        from sample import main
        app = main({})
        self.testapp = TestApp(app)

    def test_it(self):
        # No need for longer tests by putting each view in its
        # own test. Run them all here.

        res = self.testapp.get('/', status=200)
        self.assertTrue('Some' in res.body)
        self.assertTrue('This is a portlet' in res.body)

        # Default "tab" in People section
        res = self.testapp.get('/peopleosf', status=200)
        self.assertTrue('OSF Offices' in res.body)
        self.assertTrue('This is a portlet' not in res.body)

        # A report in that tab
        res = self.testapp.get('/peopleosfbaltimore', status=200)
        self.assertTrue('Baltimore Office' in res.body)
        self.assertTrue('This is a portlet' not in res.body)

        # The /communities screen
        res = self.testapp.get('/communities', status=200)
        self.assertTrue('All Communities' in res.body)
        self.assertTrue('This is a portlet' in res.body)

        # The blog in a community
        res = self.testapp.get('/communitiesblog', status=200)
        self.assertTrue('Some Blog Page' in res.body)
        self.assertTrue('This is a portlet' in res.body)

        # The test on the alternative layout, make sure it works
        res = self.testapp.get('/test', status=200)
        self.assertTrue('Some' in res.body)
        self.assertTrue('This is a portlet' not in res.body)
