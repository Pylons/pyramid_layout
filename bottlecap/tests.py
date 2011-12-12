import unittest

from pyramid import testing
from pyramid.view import render_view

from bottlecap.layout import (
    ILayoutManagerFactory,
    LayoutManager,
    add_bc_layoutmanager_factory
    )


class MainTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('bottlecap')
        self.config.add_bc_layout({'test': 'test.pt'})

    def tearDown(self):
        testing.tearDown()

    def test_add_renderer_globals(self):
        from bottlecap import add_renderer_globals

        request = testing.DummyRequest()
        event = {
            'request': request,
            'context': request.context
            }
        add_renderer_globals(event)
        settings = request.registry.settings
        self.assertTrue('bc' in settings)


class LayoutManagerTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('bottlecap')

    def test_layout(self):        
        request = testing.DummyRequest()
        lm = LayoutManager(request.context, request)
        self.assertTrue(repr(lm.layout('global'))
                .startswith('<PageTemplateFile'))

    def test_component(self):
        request = testing.DummyRequest()
        lm = LayoutManager(request.context, request)
        views = [
            'bottlecap.personal_tools',
            'bottlecap.global_nav',
            'bottlecap.search',
            'bottlecap.context_tools',
            'bottlecap.actions_menu',
            'bottlecap.column_one']
        for view in views:
            self.assertNotEqual(lm.component(view), None)

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
        