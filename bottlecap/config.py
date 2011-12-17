import inspect

from bottlecap.interfaces import IPanel
from bottlecap.layout import (
        ILayoutManagerFactory,
        LayoutManager,
        add_bc_layout,
        add_bc_layoutmanager_factory
        )

from pyramid import renderers
from pyramid.config import ConfigurationError
from pyramid.config.util import action_method
from pyramid.events import BeforeRender
from pyramid.interfaces import IRendererFactory


def add_renderer_globals(event):
    # Note that, since we have so many renderings going on now (due to
    # layout components), this gets called 8 times or so
    request = event['request']
    context = request.context
    settings = request.registry.settings
    bc = settings['bc']
    _lm = request.registry.queryUtility(ILayoutManagerFactory)
    if not _lm:
        _lm = LayoutManager
    lm = _lm(context, request)
    if 'layouts' in bc:
        lm._add_layout(bc['layouts'])
    event['lm'] = lm

    # If being called on a layout component, the econtext of the calling
    # template will be stashed away on the request.  This should be used
    # to update the globals.  It shouldn't clobber anything already added.
    econtext = getattr(request, '_parent_econtext', None)
    if econtext:
        for k, v in econtext.items():
            if k not in event:
                event[k] = v


def includeme(config):
    config.registry.settings['bc'] = {}
    config.add_directive('add_bc_layout', add_bc_layout)
    config.add_directive('add_bc_layoutmanager_factory',
            add_bc_layoutmanager_factory)
    config.add_directive('add_panel', add_panel)
    config.scan('bottlecap.panels')
    config.add_subscriber(add_renderer_globals, BeforeRender)
    config.add_static_view('bc-static', 'bottlecap:static/',
           cache_max_age=86400)


@action_method
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
        renderer = renderers.RendererHelper(
            name=renderer, package=config.package,
            registry = config.registry)

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

