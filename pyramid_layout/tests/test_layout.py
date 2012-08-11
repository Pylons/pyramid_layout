try: #pragma NO COVERAGE
    # python < 2.7
    import unittest2 as unittest
    unittest # stfu pyflakes
except ImportError: #pragma NO COVERAGE
    # python >= 2.7
    import unittest

from pyramid import testing
from pyramid_layout.layout import LayoutManager


class LayoutManagerTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_layout')

    def test_structure(self):
        from pyramid_layout.layout import Structure
        html = u'<h1>Hello</h1>'
        s = Structure(html)
        self.assertTrue(s.__html__(), html)
