try: #pragma NO COVERAGE
    # python < 2.7
    import unittest2 as unittest
except ImportError: #pragma NO COVERAGE
    # python >= 2.7
    import unittest

from pyramid import testing

from bottlecap.layout import (
    ILayoutManagerFactory,
    LayoutManager,
    )


class LayoutManagerTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('bottlecap')

    def test_layout(self):
        request = testing.DummyRequest()
        lm = LayoutManager(request.context, request)
        self.assertTrue(repr(lm.layout('global'))
                .startswith('<PageTemplateFile'))

    def test_panel(self):
        request = testing.DummyRequest()
        lm = LayoutManager(request.context, request)
        panels = [
            'bottlecap.personal_tools',
            'bottlecap.global_nav',
            'bottlecap.search',
            'bottlecap.context_tools',
            'bottlecap.actions_menu',
            'bottlecap.column_one']
        for panel in panels:
            self.assertNotEqual(lm.panel(panel), None)

    def test_app_url(self):
        request = testing.DummyRequest()
        lm = LayoutManager(request.context, request)
        self.assertEqual(lm.app_url, 'http://example.com')

    def test_context_url(self):
        request = testing.DummyRequest()
        lm = LayoutManager(request.context, request)
        self.assertEqual(lm.context_url, 'http://example.com/')

    def test_bottlecap_static(self):
        request = testing.DummyRequest()
        lm = LayoutManager(request.context, request)
        self.assertEqual(lm.bottlecap_static, 'http://example.com/bc-static/')

    def test_global_nav_menus(self):
        request = testing.DummyRequest()
        lm = LayoutManager(request.context, request)
        self.assertIsInstance(lm.global_nav_menus, list)
        self.assertEquals(lm.global_nav_menus[0]['title'], 'Item 1')

    def test_structure(self):
        from bottlecap.layout import Structure
        html = u'<h1>Hello</h1>'
        s = Structure(html)
        self.assertTrue(s.__html__(), html)

    def test_add_bc_layoutmanager_factory(self):
        class MyLayoutManager(LayoutManager):
            pass
        self.config.add_bc_layoutmanager_factory(MyLayoutManager)
        request = testing.DummyRequest()
        lm = request.registry.queryUtility(ILayoutManagerFactory)
        self.assertNotEqual(lm, None)

