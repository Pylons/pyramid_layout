try: #pragma NO COVERAGE
    # python < 2.7
    import unittest2 as unittest
except ImportError: #pragma NO COVERAGE
    # python >= 2.7
    import unittest

import mock


class Test_panel_config(unittest.TestCase):

    @mock.patch('pyramid_layout.panel.venusian')
    def test_it(self, venusian):
        from pyramid_layout.panel import panel_config as fut
        panel = object()
        with mock.patch('pyramid_layout.panel.venusian') as venusian:
            info = mock.Mock()
            info.module = 'MYMODULE'
            info.codeinfo = 'FOOCODE'
            venusian.attach.return_value = info
            decorator = fut(name='howdy')
            self.assertEqual(decorator(panel), panel)
            args, kw = venusian.attach.call_args
            self.assertEqual(kw, {'category': 'pyramid_layout'})
            venusian_wrapped, callback = args
            self.assertEqual(venusian_wrapped, panel)
            config_context = mock.Mock()
            config = mock.Mock()
            config_context.config.with_package.return_value = config
            callback(config_context, 'howdy' , panel)
            config_context.config.with_package\
                    .assert_called_once_with('MYMODULE')
            config.add_panel.assert_called_once_with(panel=panel, attr=None,
                name='howdy', renderer=None, context=None, _info='FOOCODE')

    @mock.patch('pyramid_layout.panel.venusian')
    def test_it_w_method(self, venusian):
        from pyramid_layout.panel import panel_config as fut
        panel = mock.Mock()
        panel.__name__ = 'howdy'
        with mock.patch('pyramid_layout.panel.venusian') as venusian:
            info = mock.Mock()
            info.module = 'MYMODULE'
            info.codeinfo = 'FOOCODE'
            info.scope = 'class'
            venusian.attach.return_value = info
            decorator = fut()
            self.assertEqual(decorator(panel), panel)
            args, kw = venusian.attach.call_args
            self.assertEqual(kw, {'category': 'pyramid_layout'})
            venusian_wrapped, callback = args
            self.assertEqual(venusian_wrapped, panel)
            config_context = mock.Mock()
            config = mock.Mock()
            config_context.config.with_package.return_value = config
            callback(config_context, 'howdy' , panel)
            config_context.config.with_package\
                    .assert_called_once_with('MYMODULE')
            config.add_panel.assert_called_once_with(panel=panel, attr='howdy',
                name='', renderer=None, context=None, _info='FOOCODE')

    def test_context_lookup(self):
        from pyramid_layout.config import add_panel
        from pyramid_layout.layout import LayoutManager
        from pyramid.config import Configurator
        from pyramid.testing import DummyRequest

        request = DummyRequest()
        config = Configurator()
        request.config = config
        request.registry = config.registry

        def panel_int(context, request):
            return 'panel int %s' % context
        def panel_str(context, request):
            return 'panel str %s' % context
        def panel_str_noname(context, request):
            return 'panel str noname %s' % context

        add_panel(config, panel_int, name='howdy', context=int)

        add_panel(config, panel_str, name='howdy', context=str)

        add_panel(config, panel_str_noname)
        
        config.commit()

        self.assertEqual(LayoutManager(1, request).render_panel('howdy'), 'panel int 1')
        self.assertEqual(LayoutManager(1, request).render_panel('howdy', context='1'), 'panel str 1')
        self.assertEqual(LayoutManager('2', request).render_panel('howdy'), 'panel str 2')
        self.assertEqual(LayoutManager('2', request).render_panel('howdy', context=2), 'panel int 2')
        self.assertEqual(LayoutManager('2', request).render_panel(), 'panel str noname 2')

