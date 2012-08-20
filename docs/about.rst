=====================
About Layouts, Panels
=====================

If you are writing your own UX for your Pyramid project,
Pyramid Layout provides a way to write your layout templates and logic,
register them, and use them in your view templates. As you refactor,
you can make re-usable pieces called panels for your layout and view
templates.

This section introduces the concepts of "layout" and "panel". 

About Layouts
=============

Most projects have a global look-and-feel and each view plugs into it.
In ZPT-based systems, this is usually done with a main template that
uses METAL to wrap each view's template.

Having the template, though, isn't enough. The template usually has
logic in it and needs data. Usually each view had to pass in
that data. Later, Pyramid's renderer globals provided an elegant
facility for always having certain data available in all renderings.

In Pyramid Layout, these ideas are brought together and given a name:
layout. A layout is a combination of templating and logic which wraps
up a view. With Pyramid Layout, "layout" becomes a first-class citizen with
helper config machinery and defined plug points.

In more complex projects, different parts of the same site need different
layouts. Pyramid Layout provides a way for managing the use of different
layouts in different places in your application.

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

Pyramid Layout addresses these re-usable snippets with "panels". A panel is
a box on the screen driven by templating and logic. You make panels,
register them, and you can then use them in your view templates or
layout templates.

Moreover, making and using them is a very Pythonic,
Pyramid-ic process. For example, you call your panel as a normal Python
callable and can pass it arguments.  Registration of panels, like layouts,
is very similar to registration of views in Pyramid.
