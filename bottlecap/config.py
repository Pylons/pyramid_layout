import inspect

from bottlecap.interfaces import ILayout
from bottlecap.interfaces import ILayoutManager
from bottlecap.interfaces import IPanel
from bottlecap.layout import LayoutManager

from pyramid import renderers
from pyramid.config import ConfigurationError
from pyramid.events import BeforeRender
from pyramid.events import ContextFound
from pyramid.interfaces import IRendererFactory

from zope.interface import implementedBy
from zope.interface import Interface
from zope.interface import providedBy
from zope.interface.interfaces import IInterface


def add_renderer_globals(event):
    # Note that, since we have so many renderings going on now (due to
    # panels), this gets called 8 times or so
    request = event['request']
    layout_manager = request.layout_manager
    layout = layout_manager.layout
    event['layout'] = layout
    event['main_template'] = layout.__template__
    event['panel'] = layout_manager.render_panel


def create_layout_manager(event):
    request = event.request
    context = request.context
    lm_factory = request.registry.queryUtility(ILayoutManager)
    if not lm_factory:
        lm_factory = LayoutManager
    lm = lm_factory(context, request)
    request.layout_manager = lm


def includeme(config):
    config.add_directive('add_layout', add_layout)
    config.add_directive('add_panel', add_panel)
    config.add_subscriber(add_renderer_globals, BeforeRender)
    config.add_subscriber(create_layout_manager, ContextFound)

    # Include Popper layout by default
    config.include('bottlecap.layouts.popper')


def add_panel(config, panel=None, name="", context=None,
              renderer=None, attr=None):
    """ Add a :term:`panel configuration` to the current
    configuration state.

    Arguments

    panel

      A :term:`panel callable` or a :term:`dotted Python name`
      which refers to a panel callable.  This argument is required
      unless a ``renderer`` argument also exists.  If a
      ``renderer`` argument is passed, and a ``panel`` argument is
      not provided, the panel callable defaults to a callable that
      returns an empty dictionary.

    attr

      The panel machinery defaults to using the ``__call__`` method
      of the :term:`panel callable` (or the function itself, if the
      panel callable is a function) to obtain a response.  The
      ``attr`` value allows you to vary the method attribute used
      to obtain the response.  For example, if your panel was a
      class, and the class has a method named ``index`` and you
      wanted to use this method instead of the class' ``__call__``
      method to return the response, you'd say ``attr="index"`` in the
      panel configuration for the panel.  This is
      most useful when the panel definition is a class.

    renderer

      This is either a single string term (e.g. ``json``) or a
      string implying a path or :term:`asset specification`
      (e.g. ``templates/panels.pt``) naming a :term:`renderer`
      implementation.  If the ``renderer`` value does not contain
      a dot ``.``, the specified string will be used to look up a
      renderer implementation, and that renderer implementation
      will be used to construct a response from the panel return
      value.  If the ``renderer`` value contains a dot (``.``),
      the specified term will be treated as a path, and the
      filename extension of the last element in the path will be
      used to look up the renderer implementation, which will be
      passed the full path.  The renderer implementation will be
      used to construct a :term:`response` from the panel return
      value.

      Note that if the panel itself returns a :term:`response` (see
      :ref:`the_response`), the specified renderer implementation
      is never called.

      When the renderer is a path, although a path is usually just
      a simple relative pathname (e.g. ``templates/foo.pt``,
      implying that a template named "foo.pt" is in the
      "templates" directory relative to the directory of the
      current :term:`package` of the Configurator), a path can be
      absolute, starting with a slash on UNIX or a drive letter
      prefix on Windows.  The path can alternately be a
      :term:`asset specification` in the form
      ``some.dotted.package_name:relative/path``, making it
      possible to address template assets which live in a
      separate package.

      The ``renderer`` attribute is optional.  If it is not
      defined, the "null" renderer is assumed (no rendering is
      performed and the value is passed back to the upstream
      :app:`Pyramid` machinery unmodified).

    name

      The :term:`panel name`.

    context

      An object or a :term:`dotted Python name` referring to an
      interface or class object that the :term:`context` must be
      an instance of, *or* the :term:`interface` that the
      :term:`context` must provide in order for this panel to be
      found and called.  This predicate is true when the
      :term:`context` is an instance of the represented class or
      if the :term:`context` provides the represented interface;
      it is otherwise false.
    """
    panel = config.maybe_dotted(panel)
    context = config.maybe_dotted(context)

    if not panel:
        if renderer:
            def panel(context, request):
                return {}
        else:
            raise ConfigurationError('"panel" was not specified and '
                                     'no "renderer" specified')

    if isinstance(renderer, basestring):
        renderer = renderers.RendererHelper(name=renderer,
            package=config.package, registry=config.registry)

    def register(renderer=renderer):
        if renderer is None:
            # use default renderer if one exists (reg'd in phase 1)
            if config.registry.queryUtility(IRendererFactory) is not None:
                renderer = renderers.RendererHelper(
                    name=None,
                    package=config.package,
                    registry=config.registry)

        def derive_rendered(wrapped, renderer):
            if renderer is None:
                return wrapped

            def derived(context, request, *args, **kw):
                result = wrapped(context, request, *args, **kw)
                if isinstance(result, basestring):
                    return result
                system = {'panel': panel,
                          'renderer_info': renderer,
                          'context': context,
                          'request': request
                          }
                rendered = renderer.render(result, system, request=request)
                return rendered

            return derived

        def derive_unicode(wrapped):
            def derived(context, request, *args, **kw):
                result = wrapped(context, request, *args, **kw)
                if not isinstance(result, unicode):
                    result = unicode(result, 'UTF-8')
                return result
            return derived

        derived_panel = derive_unicode(
            derive_rendered(
                _PanelMapper(attr)(panel), renderer))

        config.registry.registerAdapter(
            derived_panel, (context,), IPanel, name)

    config.action(('panel', context, name), register)


class _PanelMapper(object):

    def __init__(self, attr):
        self.attr = attr

    def __call__(self, panel):
        if inspect.isclass(panel):
            return self.map_class(panel)
        return panel

    def map_class(self, panel):
        attr = self.attr
        def class_panel(context, request):
            inst = panel(context, request)
            if attr is None:
                return inst()
            return getattr(inst, attr)()
        return class_panel


def add_layout(config, layout=None, template=None, name='', context=None,
               containment=None):
    layout = config.maybe_dotted(layout)
    context = config.maybe_dotted(context)
    containment = config.maybe_dotted(containment)

    if layout is None:
        class layout(object):
            def __init__(self, context, request):
                self.context = context
                self.request = request

    if template is None:
        raise ConfigurationError('"template" is required')

    if isinstance(template, basestring):
        helper = renderers.RendererHelper(name=template,
            package=config.package, registry=config.registry)
        template = helper.renderer.implementation()

    def register():
        def derived_layout(context, request):
            wrapped = layout(context, request)
            wrapped.__name__ = name
            wrapped.__template__ = template
            return wrapped

        r_context = context
        if r_context is None:
            r_context = Interface
        if not IInterface.providedBy(r_context):
            r_context = implementedBy(r_context)

        reg_layout = config.registry.adapters.lookup(
            (r_context,), ILayout, name=name)
        if isinstance(reg_layout, _MultiLayout):
            reg_layout[containment] = derived_layout
            return
        elif containment:
            reg_layout = _MultiLayout(reg_layout)
            reg_layout[containment] = derived_layout
        else:
            reg_layout = derived_layout

        config.registry.registerAdapter(
            reg_layout, (context,), ILayout, name=name)

    config.action(('layout', context, name, containment), register)


class _MultiLayout(dict):

    def __init__(self, default=None):
        super(_MultiLayout, self).__init__()
        self[None] = default

    def choose_layout(self, context):
        layouts = self.layouts
        node = context
        while node is not None:
            for iface in providedBy(node):
                layout = layouts.get(iface)
                if layout:
                    return layout
            for cls in type(node).mro():
                layout = layouts.get(cls)
                if layout:
                    return layout
            node = getattr(node, '__parent__', None)

        return layouts[None]

    def __call__(self, context, request):
        layout = self.choose_layout(context)
        if layout is None:
            raise KeyError # XXX What would ZCA or Pyramid raise?
        return layout(context, request)
