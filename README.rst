=========
Bottlecap
=========

When building a new Pyramid application, you might want an attractive
starting point for your UI. Bottlecap serves that purpose. Mix
Bottlecap into your Pyramid/ZPT application and use it until you get
your own UX in place.

Quick Start
===========

You can see Bottlecap added to a simple sample Pyramid app that ships
in Bottlecap:

#. Make a virtualenv as usual.

#. ``cd pyramid_bottlecap``

#. ``path/to/virtualenv/bin/python setup.py develop``

#. ``path/to/virtualenv/bin/python sample/application``

#. Open ``http://localhost:8080`` in a browser.

To see how you mix Bottlecap into your application,
just look in ``sample/application.py`` and ``sample/views.py``.

Background
==========

The Open Society Foundation commissioned a new UX for KARL,
its open source collaboration system built atop Pyramid. In particular,
the "chrome" of a UX, meaning the stuff that is part of the
application on every screen, not the content.

We wanted to develop this UX for the chrome in a productive,
fresh-start environment, to maximize the productivity of our Pyramid UI
person. So we made a new Pyramid project, with a small ZPT-oriented
application, and called it ``pyramid_bottlecap``. With this,
he could work productively while we explored the concept of "layouts."

Layouts
=======

In other systems, the "main template" or "o-wrap" is the template that
controls basic layout on all pages. We use several of these in KARL for
the major sections of the site.

But we need a little more. We need the main template, but also the
programming that supports the dynamic parts of that main template.
Let's call this combination of main template and logic for it a "layout".

Of course a large site like KARL has multiple layouts. So we need a way
to bundle a group of layouts, share component boxes between them,
and make a common template API. Let's call that the Layout Manager.

That's Bottlecap. A set of very polished templates,
the logic they depend on, and a way of choosing one of those layouts
for different parts of the site. Based on the needs of KARL,
these layouts also support "responsive design", adapting to 6 screen
sizes (large/small desktop, landscape/portrait tablet,
landscape/portrait phone.)

Reuse
=====

You need a way to get Bottlecap injected into your application. We use
Pyramid's renderer globals for that.

Next, you need a way to fill in the blanks. You don't have the same
top-level menu as KARL. You provide that by subclassing and filling in
a method.

Finally, you might want to change one individual box, aka component,
without forking the main templates or a large ZPT full of macros.
Bottlecap has a concept of components, overridden or added by standard
Python view registrations, that generate and return markup along with
the logic needed for it.

How Does It Work
================

#. Your application does a normal ``config.include`` on stuff in
``bottlecap/__init__.py``. This adds some new ``Configurator``
directives and registers a renderer global which makes an instance of
``LayoutManager`` on each render. This ``config.include`` also adds some
default views for the built-in components.

#. You then write views as normal, with ZPT templates which choose a
"layout" from the layout manager.

#. To get custom stuff into the boxes in Bottlecap,
you subclass the default ``LayoutManager``, override some methods,
and tell the ``Configurator`` to use your class instead.

#. Alternatively, you override the components by registering your own
views to override those from Bottlecap.

Extra Points
============

- Bottlecap doesn't use ZPT's METAL machinery for main template slots.
We just assume that the main template is the one and only macro used
for a layout. This means your template developers can have a more
normal looking first line.

- Ditto for components. You don't have to wrap each component in a
TAL ``define-macro``. We aren't using macros as the reuse facility.

- Unlike with ZPT macros, if one component fails, it doesn't cause the
entire page to have an exception. Just that box fails,
with a customizable error message.
