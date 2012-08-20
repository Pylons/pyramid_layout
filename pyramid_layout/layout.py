from pyramid_layout.interfaces import ILayout
from pyramid_layout.interfaces import IPanel

from pyramid.decorator import reify

import venusian
from zope.interface import providedBy

try:
    unicode = unicode  # Python 2
except NameError: #pragma no cover
    unicode = str      # Python 3


class LayoutManager(object):
    """
    An instance of LayoutManager will be available as the ``layout_manager``
    attribute of the ``request`` object in views and allows the view to access
    or change the current layout.
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def use_layout(self, name):
        """
        Makes a layout with the given name the current layout.  By default an
        unnamed layout which matches the current context and containment will be
        the current layout.  By specifying a named layout using
        :meth:`LayoutManager.use_layout`, a named view matching the current
        context, containment, and given name will be used.
        """
        layout = find_layout(self.context, self.request, name)
        setattr(self, 'layout', layout)

    @reify
    def layout(self):
        """
        Property which gets the current layout.
        """
        return find_layout(self.context, self.request)

    def render_panel(self, name, *args, **kw):
        """
        Renders the named panel, returning a `unicode` object that is the
        rendered HTML for the panel.  The panel is looked up using the current
        context and given name.  The panel is called passing in the current
        context, request and any additional parameters passed into the
        `render_panel` call.  In case a panel isn't found, `None` is returned.
        """
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
    """ A class decorator which allows a developer to create layout
    registrations.

    For example, this code in a module ``layout.py``::

      @layout_config(name='my_layout', template='mypackage:templates/layout.pt')
      class MyLayout(object):

          def __init__(self, context, request):
              self.context = context
              self.request = request

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
