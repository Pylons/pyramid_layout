=================================
About Layouts, Panels, and Popper
=================================

If you are writing your own UX for your Pyramid project,
Bottlecap provides a way to write your layout templates and logic,
register them, and use them in your view templates. As you refactor,
you can make re-usable pieces called panels for your layout and view
templates.

This section introduces the concepts of "layout" and "panel". Also,
the bundled UX known as "Popper" is explained.

About Layouts
=============

Most projects have a global look-and-feel and each view plugs into it.
In ZPT-based systems, this is usually done with a main template that
uses METAL to wrap each view's template.

Having the template, though, isn't enough. The template usually has
logic in it and needs data. Usually each view had to pass in
that data. Later, Pyramid's renderer globals provided an elegant
facility for always having certain data available in all renderings.

In Bottlecap, these ideas are brought together and given a name:
Layout. A layout is a combination of templating and logic which wraps
up a view. With Bottlecap, "layout" becomes a first-class citizen with
helper config machinery and defined plug points.

In more complex projects, different parts of the same site need
different layouts. Bottlecap provides a way for naming your layouts and
selecting them in a view.

About Panels
============

In your project you might have a number of layouts and certainly many
view templates. There is probably re-use needed for little boxes on the
screen. Or, if you are using someone else's layout, you might want to
change one small part without forking the entire template.

In ZPT, macros provide this functionality. Re-usable snippets of
templating with a marginal amount of overidability. Like main templates,
though, they also have logic and data that need to be schlepped into the
template.

Bottlecap addresses these re-usable snippets with "panels". A panel is
a box on the screen driven by templating and logic. You make panels,
register them, and you can then use them in your view templates or
layout templates.

Moreover, making and using them is a very Pythonic,
Pyramid-ic process. For example, you call your panel as a normal Python
callable and can pass it arguments.

About Popper
============

"Screw all that, I just want that slick UX that Bottlecap ships with."

Bottlecap was developed for the KARL project, building on lessons it
learned with a very large, customized-per-customer UX system. Once we
had the layout and panel machinery, we then made a UX. We decided to
ship that UX, with plug points, as a layout that all the worldwide
intertubes could use.

That layout is called Popper and it has some nice features as a
starting point for your Pyramid app:

- It's very, very attractive with a lot of attention to detail.

- We have tested it heavily across browsers, with WebTest tests and more

- We maintain it and fix bugs as part of the KARL project

- The logical structure and thus plug points are documented

- Lots of detail was paid to things like caching assets with far-future
  expires and versioned URLs, using Juicer to eliminate extra HTTP
  requests, etc.

- Slickest of all, it was built from the start with "responsive design"
  in mind, which means it adapts supernaturally for large desktops,
  small desktops, landscape tablet, portrait table, landscape phone,
  and portrait phone

.. note::

    The name "Popper" comes from
    `Karl Popper <http://en.wikipedia.org/wiki/Karl_Popper>`_,
    the economic philosopher, founder of the idea and study of open
    societies, and economics teacher to George Soros.
