try: #pragma NO COVERAGE
    # python < 2.7
    import unittest2 as unittest
    unittest # stfu pyflakes
except ImportError: #pragma NO COVERAGE
    # python >= 2.7
    import unittest


class ZCMLModuleTests(unittest.TestCase):

    def test_unicode_literals(self):
        """
        #14 Unicode literals in `zcml` module

        This test would fail under Python 3.0-3.2 if there were unicode
        literals in `zcml` module, as they were removed from the language in
        Python 3.0 and brought back in Python 3.3 by PEP 414.

        See:
            https://github.com/Pylons/pyramid_layout/pull/14
            http://www.python.org/dev/peps/pep-0414/

        """
        import pyramid_layout.zcml #pragma NO COVERAGE
