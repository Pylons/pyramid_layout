============
How It Works
============

This section breaks down the approach used by Bottlecap.

Summary
=======

What does Bottlecap do?

- Make custom Bottlecap directives available via Configurator

- Inject layouts (and a layout manager) into Pyramid
  `renderer globals <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#using-the-before-render-event>`_

- You then tell your view templates to use a layout, such as Popper

- You override static assets such as templates, images, and CSS using
  normal Pyramid overrides

- You make a custom Layout, providing a layout template and a class as
  the "Template API"

- Register panels using ``@panel_config`` and call them from your
  template expressions

In Depth
========

In your project you do a ``config.include('bottlecap')`` which makes a
number of things happen:

- Config directives are registered which let you add a layout or panel

- A ``@panel_config`` decorator is made available for
  creating/overriding panels

- The layouts, panels, and static resources in the Popper layout are
  made available

On each request, Bottlecap does some new work:

- A "layout manager" is created, which does the work of choosing which
  layout to use

- ``request.layout_manager`` gets created, which lets your application
  influence the decisions

- ``request.layout`` gets created, which points to the instance of the
  layout. This instance has all the helper methods and properties
  needed to drive the layout. If you wrote the layout,
  then you wrote this class.  XXX This is not true. There is no 
  ``request.layout``.  The layout can be accessed via i
  ``request.layout_manager.layout``.

On each rendering, Bottlecap does some more work:

- The chosen layout's instance is made available in the template

- As is the template itself

- An callable ``panel`` is available, which gives access to panels you
  might want to use in your template

So in summary:

- Bottlecap manages things called layouts and panels,
  apart from your views

- Bottlecap then makes these available in your view and template
