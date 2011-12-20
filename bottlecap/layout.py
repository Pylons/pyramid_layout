from bottlecap.interfaces import ILayout
from bottlecap.interfaces import IPanel

from pyramid.decorator import reify

from zope.interface import providedBy


class LayoutManager(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def use_layout(self, name):
        layout = find_layout(self.context, self.request, name)
        setattr(self, 'layout', layout)

    @reify
    def layout(self):
        return find_layout(self.context, self.request)

    def panel(self, name, *args, **kw):
        context = self.context
        request = self.request
        adapters = request.registry.adapters
        panel = adapters.lookup((providedBy(context),), IPanel, name=name)
        if panel is None:
            raise KeyError(name) # XXX What should we raise here?
        return Structure(panel(context, request, *args, **kw))


def find_layout(context, request, name=''):
    adapters = request.registry.adapters
    layout = adapters.lookup((providedBy(context),), ILayout, name=name)
    return layout(context, request)


class Structure(unicode):
    # Wrapping a string in this class avoids having to prefix the value
    # with `structure` in TAL

    def __html__(self):
        return self

