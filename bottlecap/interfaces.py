from zope.interface import Interface


class ILayoutManager(Interface):
    """
    Marker interface for layout manager utility.
    """


class ILayout(Interface):
    """
    Marker interface for layouts.
    """


class IPanel(Interface):

    def __call__(context, request, *args, **kw):
        """
        Return a unicode string representing HTML for a section on a larger
        page.
        """
