import unittest

from pyramid import testing
from pyramid_layout.layout import LayoutManager
from .layouts import AppLayout


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.request = testing.DummyRequest()
        self.context = testing.DummyResource()
        self.config = testing.setUp(request=self.request)
        self.config.include('pyramid_layout')
        self.request.layout_manager = LayoutManager(self.context, self.request)
        self.request.layout_manager.layout = AppLayout(self.context, self.request)

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from .views import home
        headings = self.request.layout_manager.layout.headings
        self.assertEqual(len(headings), 0)
        home(self.request)
        new_headings = [h[0] for h in headings]
        self.assertEqual(len(headings), 3)
        self.assertIn('heading-mako', new_headings)
        self.assertIn('heading-chameleon', new_headings)
        self.assertIn('heading-jinja2', new_headings)
