try: #pragma NO COVERAGE
    # python < 2.7
    import unittest2 as unittest
    unittest # stfu pyflakes
except ImportError: #pragma NO COVERAGE
    # python >= 2.7
    import unittest

import mock
from pyramid import testing

try:
    basestring = basestring  # Python 2
except NameError: #pragma no cover
    basestring = str         # Python 3
    unicode = str


class Test_add_renderer_globals(unittest.TestCase):

    def test_it(self):
        from pyramid_layout.config import add_renderer_globals
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

    def test_request_none(self):
        from pyramid_layout.config import add_renderer_globals
        request = None
        event = {
            'request': request,
            'context': None,
            }
        add_renderer_globals(event)
        self.assertEqual(len(event.keys()), 2)


class Test_create_layout_manager(unittest.TestCase):

    @mock.patch('pyramid_layout.config.LayoutManager')
    def test_it_default_factory(self, factory):
        from pyramid_layout.config import create_layout_manager as fut
        event = mock.Mock()
        event.request.registry.queryUtility.return_value = None
        fut(event)
        factory.assert_called_once_with(event.request.context, event.request)
        self.assertEqual(event.request.layout_manager, factory.return_value)

    def test_it_custom_factory(self):
        from pyramid_layout.config import create_layout_manager as fut
        event = mock.Mock()
        fut(event)
        factory = event.request.registry.queryUtility.return_value
        factory.assert_called_once_with(event.request.context, event.request)
        self.assertEqual(event.request.layout_manager, factory.return_value)


class Test_add_panel(unittest.TestCase):

    def call_fut(self, config, panel, **kw):
        from pyramid_layout.config import add_panel
        return add_panel(config, panel, **kw)

    def test_func_no_renderer(self):
        from pyramid_layout.interfaces import IPanel
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        def panel(context, request):
            return b'TEST'
        self.call_fut(config, panel)
        args, kwargs = config.action.call_args
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived(None, None)
        self.assertEqual(result, 'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        self.assertEqual(name, '')

    @mock.patch('pyramid_layout.config.renderers')
    def test_func_w_renderer_but_returns_string(self, renderers):
        from pyramid_layout.interfaces import IPanel
        renderer = mock.Mock()
        renderer.render.return_value = 'TEST'
        renderer.name = 'test_renderer.pt'
        renderers.RendererHelper.return_value = renderer
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        def panel(context, request):
            return 'TEST'
        self.call_fut(config, panel)
        args, kwargs = config.action.call_args
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived(None, None)
        self.assertEqual(result, 'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        self.assertEqual(name, '')

    @mock.patch('pyramid_layout.config.renderers')
    def test_func_w_renderer(self, renderers):
        from pyramid_layout.interfaces import IPanel
        renderer = mock.Mock()
        renderer.render.return_value = 'TEST'
        renderer.name = 'test_renderer.pt'
        renderers.RendererHelper.return_value = renderer
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        config.introspectable.return_value = introspectable = mock.Mock()
        introspectable.__setitem__ = mock.Mock()
        def panel(context, request):
            return {'body': 'TEST'}
        self.call_fut(config, panel, renderer='RENDERER')
        args, kwargs = config.action.call_args
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived('CONTEXT', 'REQUEST')
        self.assertEqual(result, 'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        renderer.render.assert_called_once_with(
            {'body': 'TEST'},
            {'panel': panel, 'renderer_info': renderer,
             'context': 'CONTEXT', 'request': 'REQUEST'},
            request='REQUEST')
        self.assertEqual(name, '')

    @mock.patch('pyramid_layout.config.renderers')
    def test_func_bypass_renderer(self, renderers):
        from pyramid_layout.interfaces import IPanel
        renderer = mock.Mock()
        renderer.name = 'test_renderer.pt'
        renderers.RendererHelper.return_value = renderer
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        config.introspectable.return_value = introspectable = mock.Mock()
        introspectable.__setitem__ = mock.Mock()
        def panel(context, request):
            return 'TEST'
        self.call_fut(config, panel, renderer='RENDERER')
        args, kwargs = config.action.call_args
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived('CONTEXT', 'REQUEST')
        self.assertEqual(result, 'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        self.assertEqual(renderer.render.call_count, 0)
        self.assertEqual(name, '')

    @mock.patch('pyramid_layout.config.renderers')
    def test_renderer_only(self, renderers):
        from pyramid_layout.interfaces import IPanel
        renderer = mock.Mock()
        renderer.render.return_value = 'TEST'
        renderer.name = 'test_renderer'
        renderers.RendererHelper.return_value = renderer
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = None
        self.call_fut(config, None, renderer='RENDERER')
        args, kwargs = config.action.call_args
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived('CONTEXT', 'REQUEST')
        self.assertEqual(result, 'TEST')
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

    @mock.patch('pyramid_layout.config.renderers')
    def test_func_w_default_renderer(self, renderers):
        from pyramid_layout.interfaces import IPanel
        renderer = mock.Mock()
        renderer.render.return_value = 'TEST'
        renderer.name = 'test_renderer'
        renderers.RendererHelper.return_value = renderer
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        config.registry.queryUtility.return_value = renderer
        def panel(context, request):
            return {'body': 'TEST'}
        self.call_fut(config, panel)
        args, kwargs = config.action.call_args
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        renderers.RendererHelper.assert_called_once_with(name=None,
            package=config.package, registry=config.registry)
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived('CONTEXT', 'REQUEST')
        self.assertEqual(result, 'TEST')
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
        from pyramid_layout.interfaces import IPanel
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
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived(None, None)
        self.assertEqual(result, 'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        self.assertEqual(name, '')

    def test_class_w_attr(self):
        from pyramid_layout.interfaces import IPanel
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
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('panel', None, ''))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {})
        derived, context, iface, name = args
        result = derived(None, None)
        self.assertEqual(result, 'TEST')
        self.assertIsInstance(result, unicode)
        self.assertEqual(context, (None,))
        self.assertEqual(iface, IPanel)
        self.assertEqual(name, '')


class Test_add_layout(unittest.TestCase):

    def call_fut(self, config, *args, **kw):
        from pyramid_layout.config import add_layout as fut
        return fut(config, *args, **kw)

    def test_no_template(self):
        from pyramid.config import ConfigurationError
        config = mock.Mock()
        with self.assertRaises(ConfigurationError):
            self.call_fut(config)

    def test_it(self):
        from pyramid_layout.interfaces import ILayout
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        template = mock.Mock()
        template.filename = 'test_template.pt'
        renderer_factory = config.registry.queryUtility.return_value
        renderer_factory.return_value.implementation.return_value = template
        self.call_fut(config, template=template, context=object)
        args, kwargs = config.action.call_args
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('layout', object, '', None))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {'name': ''})
        factory, context, iface = args
        layout = factory('context', 'request')
        self.assertEqual(layout.__layout__, '')
        self.assertEqual(layout.__template__, template)
        self.assertEqual(layout.context, 'context')
        self.assertEqual(layout.request, 'request')
        self.assertEqual(context, (object,))
        self.assertEqual(iface, ILayout)

    def test_string_template(self):
        from pyramid_layout.interfaces import ILayout
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        template = 'test_template.pt'
        renderer = mock.Mock()
        renderer.filename = 'test_template.pt'
        renderer_factory = config.registry.queryUtility.return_value
        renderer_factory.return_value.implementation.return_value = renderer
        self.call_fut(config, template=template, context=object)
        args, kwargs = config.action.call_args
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('layout', object, '', None))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {'name': ''})
        factory, context, iface = args
        layout = factory('context', 'request')
        self.assertEqual(layout.__layout__, '')
        self.assertEqual(layout.__template__, renderer)
        self.assertEqual(layout.context, 'context')
        self.assertEqual(layout.request, 'request')
        self.assertEqual(context, (object,))
        self.assertEqual(iface, ILayout)

    def test_multi_layout(self):
        from pyramid.exceptions import PredicateMismatch
        from pyramid_layout.interfaces import ILayout
        class Container(object):
            pass
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        template = mock.Mock()
        template.filename = 'test_layout.pt'
        renderer_factory = config.registry.queryUtility.return_value
        renderer_factory.return_value.implementation.return_value = template
        config.registry.adapters.lookup.return_value = None

        self.call_fut(config, template=template, containment=Container,
                      name='foo')
        args, kwargs = config.action.call_args
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('layout', None, 'foo', Container))
        register()
        args, kwargs = config.registry.registerAdapter.call_args
        self.assertEqual(kwargs, {'name': 'foo'})
        factory, context, iface = args
        with self.assertRaises(PredicateMismatch):
            # Context of type 'str' won't match containment
            layout = factory('context', 'request')
        container = Container()
        layout = factory(container, 'request')
        self.assertEqual(layout.__layout__, 'foo')
        self.assertEqual(layout.__template__, template)
        self.assertEqual(layout.context, container)
        self.assertEqual(layout.request, 'request')
        self.assertEqual(context, (None,))
        self.assertEqual(iface, ILayout)

    def test_second_multi_layout(self):
        from pyramid_layout.config import _MultiLayout
        from zope.interface import implementer
        from zope.interface import Interface
        class IContainer(Interface):
            pass
        @implementer(IContainer)
        class Container(object):
            pass
        config = mock.Mock()
        config.maybe_dotted = lambda x: x
        template = mock.Mock()
        template.filename = 'test_template.pt'
        renderer_factory = config.registry.queryUtility.return_value
        renderer_factory.return_value.implementation.return_value = template
        multi = _MultiLayout()
        config.registry.adapters.lookup.return_value = multi

        self.call_fut(config, template=template, containment=IContainer,
                      name='foo')
        args, kwargs = config.action.call_args
        self.assertIn('introspectables', kwargs)
        discriminator, register = args
        self.assertEqual(discriminator, ('layout', None, 'foo', IContainer))
        register()
        container = Container()
        layout = multi(container, 'request')
        self.assertEqual(layout.__layout__, 'foo')
        self.assertEqual(layout.__template__, template)
        self.assertEqual(layout.context, container)
        self.assertEqual(layout.request, 'request')
