Using Pyramid Layout
====================

To get started with Pyramid Layout, include :mod:`pyramid_layout` in your 
application's config::

    config = Configurator(...)
    config.include('pyramid_layout')

Alternately, instead of using the
:ref:`the Configurator's <pyramid:configuration_narr>`
include method, you can
activate Pyramid Layout by changing your application’s .ini file, 
using the following line::

    pyramid.includes = pyramid_layout

Including ``pyramid_layout`` in your application adds two new directives to
your :pyramid:term:`configurator`: :meth:`add_layout
<pyramid_layout.config.add_layout>` and :meth:`add_panel
<pyramid_layout.config.add_panel>`.  These directives work very much like
``add_view`` but add registrations for layouts and panels.  Including
``pyramid_layout`` will also add an attribute, ``layout_manager``, to the
request object of each request, which is an instance of
:class:`pyramid_layout.layout.LayoutManager`.

Finally, three renderer globals are added which will be available to all
templates: ``layout``, ``main_template``, and ``panel``.  ``layout`` is an
instance of the layout selected for the view.  ``main_template`` is the
template object that provides the main layout (aka, owrap) for the view.
``panel``, a shortcut for
:meth:`pyramid_layout.layout.LayoutManager.render_panel`,  is a callable used
to render panels in your templates.

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
            return has_permission(self.request, 'manage')

An instance of the layout object will be available in templates as the
renderer global, ``layout``. For example, if you are using Mako or ZPT
for templating, you can put something like this in a template::

    <title>${layout.page_title}</title>

For Jinja2::

    <title>{{layout.page_title}}</title>


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

Now that you have a layout, time to use it on a particular view. To use
a named layout, call the ``use_layout`` method of ``LayoutManager`` in
your view::

    def myview(context, request):
        request.layout_manager.use_layout('admin')
        ...

The decorator
:func:`pyramid_layout.layout.layout_config` can be used in conjuction
with
:meth:`pyramid.config.Configurator.scan <pyramid:pyramid.config.Configurator.scan>`
to register layouts declaratively::

    from pyramid_layout.layout import layout_config

    @layout_config(template='templates/default_layout.pt')
    @layout_config(name='admin', template='templates/admin_layout.pt')
    class MyLayout(object):
        ...

Layouts can also be registered for specific context types and
containments. See the :ref:`api docs <apidocs>` for more info.

Using Panels
------------

A panel is similar to a view but is responsible for rendering only a part of a
page.  A panel is a callable which can accept arbitrary arguments (the first 
two are always ``context`` and ``request``) and either returns an html string or
uses a Pyramid renderer to render the html to insert in the page.

.. note::

    You can mix-and-match template languages in a project. Some panels
    can be implemented in Jinja2, some in Mako, some in ZPT. All can
    work in layouts implemented in any template language supported by
    Pyramid Layout.

A panel can be configured using the method, ``add_panel`` of the 
``Configurator`` instance::

    config.add_panel('myproject.layout.siblings_panel', 'siblings',
                     renderer='myproject.layout:templates/siblings.pt')

Because panels can be called with arguments, they can be parameterized
when used in different ways. The panel callable might look something
like::

    def siblings_panel(context, request, n_siblings=5):
        return [sibling for sibling in context.__parent__.values()
                if sibling is not context][:n_siblings]

And could be called from a template like this::

    ${panel('siblings', 8)}  <!-- Show 8 siblings -->

If using ``Configurator.scan``, you can also register the panel
declaratively::

    from pyramid_layout.panel import panel_config

    @panel_config('siblings', renderer='templates/siblings.pt')
    def siblings_panel(context, request, n_siblings=5):
        return [sibling for sibling in context.__parent__.values()
                if sibling is not context][:n_siblings]

Panels can be registered to match only specific context types.  See
the :ref:`api docs <apidocs>` for more info.

View Templates and Layouts in ZPT
=================================

If you are a ZPT user, connecting your view template to the layout and
its template is pretty easy. Just make this your first line in your
view template:

.. code-block:: xml

  <metal:block use-macro="main_template">

That's a little different than what ZPT users are used to seeing,
which is more like:

.. code-block:: xml

  <metal:block use-macro="main_template.macros['master']">

In fact, the template used by the layout *doesn't need* a
``<metal:block define-macro="main_template">`` at all. Why? Here is
what Pyramid Layout is doing:

- @layout_config takes the ZPT for the master template and lets you
  call it as a macro

- Pyramid Layout then uses Pyramid's renderer globals to make that main
  template available, as a callable macro, under the special name
  ``main_template``

- This ``main_template`` macro is available in the global namespace of
  your template

After that, it's about what you'd expect. The main template has to
define at least one slot. The view template has to fill at least one
slot.
