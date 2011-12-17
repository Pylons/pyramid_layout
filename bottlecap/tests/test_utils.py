try: #pragma NO COVERAGE
    import unittest2 as unittest
except ImportError: #pragma NO COVERAGE
    import unittest
import mock

from pyramid import testing


class GetMicrotemplatesTestCase(unittest.TestCase):

    def call_fut(self, names=None):
        from bottlecap.utils import get_microtemplates
        return get_microtemplates(names=names)

    def test_it(self):
        import os
        _here = os.path.dirname(__file__)
        _microtemplates = os.path.join(_here, 'microtemplates')
        with mock.patch('bottlecap.utils._microtemplates', _microtemplates):

            # Just test it without names, as it is not yet implemented
            templates = self.call_fut()
            # ... and we get all templates anyway.
            self.assertEqual(templates, {
                'a': 'MICROTEMPLATE a.mustache\n',
                'b': 'MICROTEMPLATE b.mustache\n',
                })

