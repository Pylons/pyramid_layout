try: #pragma NO COVERAGE
    # python < 2.7
    import unittest2 as unittest
    unittest # pyflakes stfu
except ImportError: #pragma NO COVERAGE
    # python >= 2.7
    import unittest

from pyramid import testing


class TestPopperLayout(unittest.TestCase):

    def make_one(self, context, request):
        from bottlecap.layouts.popper.layout import PopperLayout
        return PopperLayout(context, request)


class TestPanels(unittest.TestCase):

    def setUp(self):
        from bottlecap.config import create_layout_manager
        config = testing.setUp()
        config.include('bottlecap')
        context = None
        self.request = request = testing.DummyRequest()
        request.context = context
        request.request = request
        create_layout_manager(request)

    def test_personal_tools(self):
        lm = self.request.layout_manager
        self.assertTrue(lm.render_panel('popper.personal_tools'))

