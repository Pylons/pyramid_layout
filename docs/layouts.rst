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

Including :mod:`pyramid_layout` in your application adds two new directives
to your :pyramid:term:`configurator`: :meth:`add_layout
<pyramid_layout.config.add_layout>` and :meth:`add_panel
<pyramid_layout.config.add_panel>`.  These directives work very much like
:meth:`add_view <pyramid:pyramid.config.Configurator.add_view>`, but add
registrations for layouts and panels.  Including :mod:`pyramid_layout` will
also add an attribute, ``layout_manager``, to the request object of each
request, which is an instance of :class:`LayoutManager
<pyramid_layout.layout.LayoutManager>`.

Finally, three renderer globals are added which will be available to all
templates: ``layout``, ``main_template``, and ``panel``.  ``layout`` is an
instance of the :term:`layout class` of the current layout.  ``main_template``
is the template object that provides the :term:`main template` (aka, o-wrap)
for the view.  ``panel``, a shortcut for :meth:`LayoutManager.render_panel
<pyramid_layout.layout.LayoutManager.render_panel>`,  is a callable used to
render :term:`panels <panel>` in your templates.

Using Layouts
-------------

A :term:`layout` consists of a :term:`layout class` and :term:`main template`.
The layout class will be instantiated on a per request basis with the context
and request as arguments.  The layout class can be omitted, in which case a
default layout class will be used, which only assigns `context` and `request`
to the layout instance.  Generally, though, you will provide your own layout
class which can serve as a place to provide API that will be available to your
templates.  A simple layout class might look like::

    class MyLayout(object):
        page_title = 'Hooray! My App!'

        def __init__(self, context, request):
            self.context = context
            self.request = request
            self.home_url = request.application_url

        def is_user_admin(self):
            return has_permission(self.request, 'manage')

A :term:`layout instance` will be available in templates as the
renderer global, ``layout``. For example, if you are using Mako or ZPT
for templating, you can put something like this in a template::

    <title>${layout.page_title}</title>

For Jinja2::

    <title>{{layout.page_title}}</title>


All :term:`layouts <layout>` must have an associated template which is the
:term:`main template` for the layout and will be present as ``main_template``
in renderer globals.

To register a layout, use the :meth:`add_layout
<pyramid_layout.config.add_layout>` method of the configurator::

    config.add_layout('myproject.layout.MyLayout', 
                      'myproject.layout:templates/default_layout.pt')

The above registered layout will be the default layout.  Layouts can also be 
named::

    config.add_layout('myproject.layout.MyLayout', 
                      'myproject.layout:templates/admin_layout.pt',
                      name='admin')

Now that you have a layout, time to use it on a particular view. Layouts can
be defined declaratively, next to your renderer, in the view configuration::

    @view_config(..., layout='admin')
    def myview(context, request):
        ...

In Pyramid < 1.4, to use a named layout, call
:meth:`LayoutManager.use_layout
<pyramid_layout.layout.LayoutManager.use_layout>` method in your view::

    def myview(context, request):
        request.layout_manager.use_layout('admin')
        ...

If you are using :pyramid:term:`traversal` you may find that in most cases it
is unnecessary to name your layouts.  Use of the `context` argument to the
layout configuration can allow you to use a particular layout whenever the
:pyramid:term:`context` is of a particular type::

    from ..models.wiki import WikiPage

    config.add_layout('myproject.layout.MyLayout', 
                      'myproject.layout:templates/wiki_layout.pt',
                      context=WikiPage)

Similarly, the `containment` argument allows you to use a particular layout for
an entire branch of your :pyramid:term:`resource tree`::

    from ..models.admin import AdminFolder

    config.add_layout('myproject.layout.MyLayout', 
                      'myproject.layout:templates/admin_layout.pt',
                      containment=AdminFolder)

The decorator :func:`layout_config <pyramid_layout.layout.layout_config>` can
be used in conjuction with :meth:`Configurator.scan
<pyramid:pyramid.config.Configurator.scan>` to register layouts declaratively::

    from pyramid_layout.layout import layout_config

    @layout_config(template='templates/default_layout.pt')
    @layout_config(name='admin', template='templates/admin_layout.pt')
    class MyLayout(object):
        ...

Layouts can also be registered for specific context types and
containments. See the :ref:`api docs <apidocs>` for more info.

Using Panels
------------

A :term:`panel` is similar to a view but is responsible for rendering only a
part of a page.  A panel is a callable which can accept arbitrary arguments
(the first two are always ``context`` and ``request``) and either returns an
html string or uses a Pyramid renderer to render the html to insert in the
page.

.. note::

    You can mix-and-match template languages in a project. Some panels
    can be implemented in Jinja2, some in Mako, some in ZPT. All can
    work in layouts implemented in any template language supported by
    Pyramid Layout.

A :term:`panel` can be configured using the method, ``add_panel`` of the 
``Configurator`` instance::

    config.add_panel('myproject.layout.siblings_panel', 'siblings',
                     renderer='myproject.layout:templates/siblings.pt')

Because :term:`panels <panel>` can be called with arguments, they can be
parameterized when used in different ways. The panel callable might look
something like::

    def siblings_panel(context, request, n_siblings=5):
        return [sibling for sibling in context.__parent__.values()
                if sibling is not context][:n_siblings]

And could be called from a template like this::

    ${panel('siblings', 8)}  <!-- Show 8 siblings -->

If using :meth:`Configurator.scan <pyramid:pyramid.config.Configurator.scan>`,
you can also register the panel declaratively::

    from pyramid_layout.panel import panel_config

    @panel_config('siblings', renderer='templates/siblings.pt')
    def siblings_panel(context, request, n_siblings=5):
        return [sibling for sibling in context.__parent__.values()
                if sibling is not context][:n_siblings]

Like :term:`layouts <layout>`, :term:`panels <panel>` can also be registered
for a context type::

    from pyramid_layout.panel import panel_config

    @panel_config(name='see-also'
                  context='myproject.models.Document', 
                  renderer='templates/see-also.pt')
    def see_also(context, request):
        return {'title': context.title,
                'url': request.resource_url(context)}

The context to use to look up a panel defaults to the :pyramid:term:`context`
found during :pyramid:term:`traversal`.  A different context may be provided by
passing a `context` keyword argument to panel call.  In this hypothetical
template, each `related_content` item can potentially be a different type and
wind up invoking a different panel::

    <h2>Related Content</h2>
    <ul>
      <li tal:repeat="item releated_content">
        ${panel('see-also', context=item)}
      </li>
    </ul>

When registering panels by context, the `name` part of the registration becomes
optional.  In the example above, we could make the `see-also` panels the 
default panels for any registered contexts by simply omitting `name`::

    from pyramid_layout.panel import panel_config

    @panel_config(context='myproject.models.Document', 
                  renderer='templates/see-also.pt')
    def see_also(context, request):
        return {'title': context.title,
                'url': request.resource_url(context)}

Also in the template::

    <h2>Related Content</h2>
    <ul>
      <li tal:repeat="item releated_content">
        ${panel(context=item)}
      </li>
    </ul>

See the :ref:`api docs <apidocs>` for more info.

Using the Main Template
-----------------------

The precise syntax for hooking into the :term:`main template` from a view 
template varies depending on the templating language you're using.

ZPT
~~~

If you are a ZPT user, connecting your view template to the :term:`layout` and
its :term:`main template` is pretty easy. Just make this the outermost element
in your view template:

.. code-block:: xml

  <metal:block use-macro="main_template">
  ...
  </metal:block>

You'll note that we're taking advantage of a feature in Chameleon that allows
us to `use a template instance as a macro
<http://chameleon.repoze.org/docs/latest/reference.html#id46>`_ without having
to explicitly define a macro in the :term:`main template`.

After that, it's about what you'd expect. The :term:`main template` has to
define at least one slot. The view template has to fill at least one slot.

Mako
~~~~

In Mako, to use the :term:`main template` from your :term:`layout`, use this as
the first line in your view template:

.. code-block:: xml

  <%inherit file="${context['main_template'].uri}"/>

In your :term:`main template`, insert this line at the point where you'd like
for the view template to be inserted:

.. code-block:: xml

  ${next.body()}

Jinja2
~~~~~~

For Jinja2, to use the :term:`main template` for your :term:`layout`, use this
as the first line in your view template:

.. code-block:: xml

  {% extends main_template %}

From there, blocks defined in your :term:`main template` can be overridden by
blocks defined in your view template, per normal usage.
