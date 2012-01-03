try: #pragma NO COVERAGE
    # python < 2.7
    import unittest2 as unittest
except ImportError: #pragma NO COVERAGE
    # python >= 2.7
    import unittest


class TestPopperLayout(unittest.TestCase):

    def make_one(self, context, request):
        from bottlecap.layouts.popper.layout import PopperLayout
        return PopperLayout(context, request)
