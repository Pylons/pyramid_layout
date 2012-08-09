try: #pragma NO COVERAGE
    # python < 2.7
    import unittest2 as unittest
except ImportError: #pragma NO COVERAGE
    # python >= 2.7
    import unittest

from pyramid import testing
from pyramid_layout.layout import LayoutManager


class LayoutManagerTests(unittest.TestCase):
    # This is pretty leaky as a unittest, as we wind up testing the whole
    # registration framework for the default Popper layout.

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_layout')

    def test_layout(self):
        from pyramid_layout.layouts.popper.layout import PopperLayout
        request = testing.DummyRequest()
        lm = LayoutManager(request.context, request)
        self.assertIsInstance(lm.layout, PopperLayout)

    def test_render_panel(self):
        request = testing.DummyRequest()
        request.layout_manager = lm = LayoutManager(request.context, request)
        panels = [
            'popper.personal_tools',
            'popper.global_nav',
            'popper.search',
            'popper.context_tools',
            'popper.actions_menu',
            'popper.column_one']
        for panel in panels:
            self.assertNotEqual(lm.render_panel(panel), None)
        self.assertEqual(lm.render_panel('does_not_exist'), None)

    def test_use_layout(self):
        request = testing.DummyRequest()
        request.layout_manager = lm = LayoutManager(request.context, request)
        self.config.add_layout(name='test',
            template='pyramid_layout.layouts.popper:templates/popper_layout.pt')
        self.assertEqual(lm.layout.__layout__, '')
        lm.use_layout('test')
        self.assertEqual(lm.layout.__layout__, 'test')

    def test_structure(self):
        from pyramid_layout.layout import Structure
        html = u'<h1>Hello</h1>'
        s = Structure(html)
        self.assertTrue(s.__html__(), html)
