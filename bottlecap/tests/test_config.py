try: #pragma NO COVERAGE
    # python < 2.7
    import unittest2 as unittest
except ImportError: #pragma NO COVERAGE
    # python >= 2.7
    import unittest

import mock
from pyramid import testing


class Test_add_renderer_globals(unittest.TestCase):

    def test_it(self):
        from bottlecap.config import add_renderer_globals
        lm = mock.Mock()
        request = testing.DummyRequest()
        request.registry.settings = {'bc': {}}
        request.layout_manager = lm
        lm.layout.__template__ = 'TEMPLATE'
        event = {
            'request': request,
            'context': request.context
            }
        add_renderer_globals(event)
        settings = request.registry.settings
        self.assertIn('bc', settings)
        self.assertIn('panel', event)
        self.assertEqual(event['layout'], lm.layout)
        self.assertEqual(event['main_template'], 'TEMPLATE')


class Test_add_panel(unittest.TestCase):

    def call_fut(self, config, panel, **kw):
        from bottlecap.config import add_panel
        return add_panel(config, panel, **kw)

    def test_func_no_renderer(self):
        from bottlecap.interfaces import IPanel
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        def panel(context, request):
            return 'TEST'
        self.call_fut(config, panel)
        args, kwargs = config.action.call_args
        self.assertEqual(kwargs, {})
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived(None, None)
        self.assertEqual(result, u'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        self.assertEqual(name, '')

    @mock.patch('bottlecap.config.renderers')
    def test_func_w_renderer(self, renderers):
        from bottlecap.interfaces import IPanel
        renderer = mock.Mock()
        renderer.render.return_value = 'TEST'
        renderers.RendererHelper.return_value = renderer
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        def panel(context, request):
            return {'body': 'TEST'}
        self.call_fut(config, panel, renderer='RENDERER')
        renderers.RendererHelper.assert_called_once_with(name='RENDERER',
            package=config.package, registry=config.registry)
        args, kwargs = config.action.call_args
        self.assertEqual(kwargs, {})
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived('CONTEXT', 'REQUEST')
        self.assertEqual(result, u'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        renderer.render.assert_called_once_with(
            {'body': 'TEST'},
            {'panel': panel, 'renderer_info': renderer,
             'context': 'CONTEXT', 'request': 'REQUEST'},
            request='REQUEST')
        self.assertEqual(name, '')

    @mock.patch('bottlecap.config.renderers')
    def test_func_bypass_renderer(self, renderers):
        from bottlecap.interfaces import IPanel
        renderer = mock.Mock()
        renderers.RendererHelper.return_value = renderer
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        def panel(context, request):
            return 'TEST'
        self.call_fut(config, panel, renderer='RENDERER')
        renderers.RendererHelper.assert_called_once_with(name='RENDERER',
            package=config.package, registry=config.registry)
        args, kwargs = config.action.call_args
        self.assertEqual(kwargs, {})
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived('CONTEXT', 'REQUEST')
        self.assertEqual(result, u'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        self.assertEqual(renderer.render.call_count, 0)
        self.assertEqual(name, '')

    @mock.patch('bottlecap.config.renderers')
    def test_renderer_only(self, renderers):
        from bottlecap.interfaces import IPanel
        renderer = mock.Mock()
        renderer.render.return_value = 'TEST'
        renderers.RendererHelper.return_value = renderer
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        self.call_fut(config, None, renderer='RENDERER')
        renderers.RendererHelper.assert_called_once_with(name='RENDERER',
            package=config.package, registry=config.registry)
        args, kwargs = config.action.call_args
        self.assertEqual(kwargs, {})
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived('CONTEXT', 'REQUEST')
        self.assertEqual(result, u'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        self.assertEqual(name, '')

    def test_no_panel_or_renderer(self):
        from pyramid.exceptions import ConfigurationError
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        with self.assertRaises(ConfigurationError):
            self.call_fut(config, None)

    @mock.patch('bottlecap.config.renderers')
    def test_func_w_default_renderer(self, renderers):
        from bottlecap.interfaces import IPanel
        renderer = mock.Mock()
        renderer.render.return_value = 'TEST'
        renderers.RendererHelper.return_value = renderer
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = renderer
        def panel(context, request):
            return {'body': 'TEST'}
        self.call_fut(config, panel)
        args, kwargs = config.action.call_args
        self.assertEqual(kwargs, {})
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        renderers.RendererHelper.assert_called_once_with(name=None,
            package=config.package, registry=config.registry)
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived('CONTEXT', 'REQUEST')
        self.assertEqual(result, u'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        renderer.render.assert_called_once_with(
            {'body': 'TEST'},
            {'panel': panel, 'renderer_info': renderer,
             'context': 'CONTEXT', 'request': 'REQUEST'},
            request='REQUEST')
        self.assertEqual(name, '')

    def test_class_no_attr(self):
        from bottlecap.interfaces import IPanel
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        class Panel(object):
            def __init__(self, context, request):
                pass
            def __call__(self):
                return 'TEST'
        self.call_fut(config, Panel)
        args, kwargs = config.action.call_args
        self.assertEqual(kwargs, {})
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived(None, None)
        self.assertEqual(result, u'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        self.assertEqual(name, '')

    def test_class_w_attr(self):
        from bottlecap.interfaces import IPanel
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        class Panel(object):
            def __init__(self, context, request):
                pass
            def panel(self):
                return 'TEST'
        self.call_fut(config, Panel, attr='panel')
        args, kwargs = config.action.call_args
        self.assertEqual(kwargs, {})
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived(None, None)
        self.assertEqual(result, u'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        self.assertEqual(name, '')


