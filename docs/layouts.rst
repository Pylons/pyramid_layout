Using Pyramid Layout
====================

To get started with Pyramid Layout, include ``pyramid_layout`` in your 
application's config::

    config = Configurator(...)
    config.include('pyramid_layout')

Alternately, instead of using the Configurator’s include method, you can 
activate Pyramid Layout by changing your application’s .ini file, 
use the following line::

    pyramid.includes = pyramid_layout

Including ``pyramid_layout`` in your application adds two new directives to your
configurator: ``add_layout`` and ``add_panel``.  These directives work very much
like ``add_view`` but add registrations for layouts and panels.  Including 
``pyramid_layout`` will also add an attribute, ``layout_manager``, to the 
request object of each request, which is an instance of 
``pyramid_layout.layout.LayoutManager``.  Finally, three renderer globals are
added which will be available to all templates: ``layout``, ``main_template``,
and ``panel``.  ``layout`` is an instance of the layout selected for the view.
``main_template`` is the template object that provides the main layout (aka,
owrap) for the view.  ``panel`` is a callable used to render panels in your
templates.

Using Layouts
-------------

A layout consists of a class and template.  The layout class will be 
instantiated on a per request basis with the context and request as arguments.
The layout class can be omitted, in which case a default layout class will be
used, which only assigns `context` and `request` to the layout instance.  
Generally, though, you will provide your own layout class which can serve as a
place to provide API that will be available to your templates.  A simple layout
class might look like::

    class MyLayout(object):
        page_title = 'Hooray! My App!'

        def __init__(self, context, request):
            self.context = context
            self.request = request
            self.home_url = request.application_url

        def is_user_admin(self):
            return has_permission(request, 'manage')

An instance of the layout object will be available in templates as the renderer
global, ``layout``, so, for example, you can put something like this in a
template::

    <title>${layout.page_title}</title>

All layouts must have an associated template which is the main template for the
layout and will be present as ``main_template`` in renderer globals.

To register a layout, use the ``add_layout`` method of the configurator::

    config.add_layout('myproject.layout.MyLayout', 
                      'myproject.layout:templates/default_layout.pt')

The above registered layout will be the default layout.  Layouts can also be 
named::

    config.add_layout('myproject.layout.MyLayout', 
                      'myproject.layout:templates/admin_layout.pt',
                      name='admin')

To use a named layout, call the ``use_layout`` method of ``LayoutManager`` in 
your view::

    def myview(context, request):
        request.layout_manager.use_layout('admin')
        ...

The decorator ``pyramid_layout.layout.layout_config`` can be used in conjuction
with ``pyramid.config.Configurator.scan`` to register layouts declaratively::

    from pyramid_layout.layout import layout_config

    @layout_config(template='templates/default_layout.pt')
    @layout_config(name='admin', template='templates/admin_layout.pt')
    class MyLayout(object):
        ...

Layouts can also be registered for specific context types and containments. See
the api docs for more info.

Using Panels
------------

A panel is similar to a view but is responsible for rendering only a part of a
page.  A panel is a callable which can accept arbitrary arguments (the first 
two are always ``context`` and ``request``) and either returns an html string or
uses a Pyramid renderer to render the html to insert in the page.  

A panel can be configured using the method, ``add_panel`` of the 
``Configurator`` instance::

    config.add_panel('myproject.layout.siblings_panel', 'siblings',
                     renderer='myproject.layout:templates/siblings.pt')

The panel callable might look something like::

    def siblings_panel(context, request, n_siblings=5):
        return [sibling for sibling in context.__parent__.values()
                if sibling is not context][:n_siblings]

And could be called from a template like this::

    ${panel('siblings', 8)}  <!-- Show 8 siblings -->

If using ``Configurator.scan``, you can also register the panel declaratively::

    from pyramid_layout.panel import panel_config

    @panel_config('siblings', renderer='templates/siblings.pt')
    def siblings_panel(context, request, n_siblings=5):
        return [sibling for sibling in context.__parent__.values()
                if sibling is not context][:n_siblings]

Panels can be registered to match only specific context types.  See api docs for
more info.

