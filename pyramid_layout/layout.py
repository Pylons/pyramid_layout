from pyramid_layout.interfaces import ILayout
from pyramid_layout.interfaces import IPanel

from pyramid.decorator import reify

import venusian
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

    def render_panel(self, name, *args, **kw):
        context = self.context
        request = self.request
        adapters = request.registry.adapters
        panel = adapters.lookup((providedBy(context),), IPanel, name=name)
        if panel is None:
            # Mimics behavior of pyramid.view.render_view
            return None
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


class layout_config(object):
    """ A function, class or method :term:`decorator` which allows a
    developer to create layout registrations.

    For example, this code in a module ``layout.py``::

      @layout_config(name='my_layout', template='mypackage:templates/layout.pt')
      def my_layout(context, request):
          return 'OK'

    The following arguments are supported as arguments to
    :class:`pyramid_layout.layout.layout_config`: ``context``, ``name``,
    ``template``, ``containment``.

    The meanings of these arguments are the same as the arguments passed to
    :meth:`pyramid_layout.config.add_layout`.
    """
    def __init__(self, name='', context=None, template=None, containment=None):
        self.name = name
        self.context = context
        self.template = template
        self.containment = containment

    def __call__(self, wrapped):
        settings = self.__dict__.copy()

        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_layout(layout=ob, **settings)

        info = venusian.attach(wrapped, callback, category='pyramid_layout')

        settings['_info'] = info.codeinfo # fbo "action_method"
        return wrapped
