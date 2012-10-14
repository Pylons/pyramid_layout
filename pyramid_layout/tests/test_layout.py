try: #pragma NO COVERAGE
    # python < 2.7
    import unittest2 as unittest
    unittest # stfu pyflakes
except ImportError: #pragma NO COVERAGE
    # python >= 2.7
    import unittest

import mock
from pyramid import testing


class LayoutManagerTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_layout')

    def make_one(self, context, request):
        from pyramid_layout.layout import LayoutManager as test_class
        return test_class(context, request)

    @mock.patch('pyramid_layout.layout.find_layout')
    def test_use_layout(self, find_layout):
        lm = self.make_one('context', 'request')
        find_layout.return_value = 'Test Layout'
        lm.use_layout('test')
        self.assertEqual(lm.layout, 'Test Layout')
        find_layout.assert_called_once_with('context', 'request', 'test')

    @mock.patch('pyramid_layout.layout.find_layout')
    def test_layout(self, find_layout):
        lm = self.make_one('context', 'request')
        find_layout.return_value = 'Test Layout'
        self.assertEqual(lm.layout, 'Test Layout')
        self.assertEqual(lm.layout, 'Test Layout')
        find_layout.assert_called_once_with('context', 'request')

    def test_render_panel(self):
        from zope.interface import providedBy
        from pyramid_layout.interfaces import IPanel
        request = mock.Mock()
        lookup = request.registry.adapters.lookup
        panel = lookup.return_value
        panel.return_value = 'Test Panel'
        lm = self.make_one('context', request)
        self.assertEqual(lm.render_panel('test'), 'Test Panel')
        lookup.assert_called_once_with(
            (providedBy('context'),), IPanel, name='test')
        panel.assert_called_once_with('context', request)

    def test_render_panel_with_args(self):
        from zope.interface import providedBy
        from pyramid_layout.interfaces import IPanel
        request = mock.Mock()
        lookup = request.registry.adapters.lookup
        panel = lookup.return_value
        panel.return_value = 'Test Panel'
        lm = self.make_one('context', request)
        self.assertEqual(lm.render_panel('test', 1, two=3), 'Test Panel')
        lookup.assert_called_once_with(
            (providedBy('context'),), IPanel, name='test')
        panel.assert_called_once_with('context', request, 1, two=3)

    def test_render_panel_no_panel(self):
        from zope.interface import providedBy
        from pyramid_layout.interfaces import IPanel
        request = mock.Mock()
        lookup = request.registry.adapters.lookup
        lookup.return_value = None
        lm = self.make_one('context', request)
        self.assertEqual(lm.render_panel('test'), None)
        lookup.assert_called_once_with(
            (providedBy('context'),), IPanel, name='test')

    @mock.patch('pyramid_layout.layout.find_layout')
    def test_layout_predicate(self, find_layout):
        from pyramid_layout.config import LayoutPredicate
        lm = self.make_one('context', 'request')
        find_layout.return_value = 'Test Layout'
        pred = LayoutPredicate('test', None)
        class Request(object):
            pass
        request = Request()
        request.layout_manager = lm
        result = pred(None, request)
        self.assertTrue(result)
        self.assertEqual(lm.layout, 'Test Layout')
        self.assertEqual(pred.text(), 'layout = test')
        find_layout.assert_called_once_with('context', 'request', 'test')


class Test_find_layout(unittest.TestCase):

    def test_it(self):
        from zope.interface import providedBy
        from pyramid_layout.interfaces import ILayout
        from pyramid_layout.layout import find_layout
        request = mock.Mock()
        lookup = request.registry.adapters.lookup
        Layout = lookup.return_value
        find_layout('context', request, 'test')
        Layout.assert_called_once_with('context', request)
        lookup.assert_called_once_with(
            (providedBy('context'),), ILayout, name='test')


class TestStructure(unittest.TestCase):

    def test_it(self):
        from pyramid_layout.layout import Structure
        html = '<h1>Hello</h1>'
        s = Structure(html)
        self.assertTrue(s.__html__(), html)


class Test_layout_config(unittest.TestCase):

    @mock.patch('pyramid_layout.layout.venusian')
    def test_it(self, venusian):
        from pyramid_layout.layout import layout_config
        decorator = layout_config('name', 'context', 'template', 'containment')
        self.assertEqual(decorator('wrapped'), 'wrapped')
        info = venusian.attach.return_value
        args, kwargs = venusian.attach.call_args
        self.assertEqual(kwargs, {'category': 'pyramid_layout'})
        wrapped, callback = args
        self.assertEqual(wrapped, 'wrapped')
        context = mock.Mock()
        context.config.with_package.return_value = context
        callback(context, 'name', 'layout')
        context.config.with_package.assert_called_once_with(info.module)
        context.add_layout.assert_called_once_with(
            layout='layout',
            name='name',
            context='context',
            template='template',
            containment='containment',
            _info=info.codeinfo)
