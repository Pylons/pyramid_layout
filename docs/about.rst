=====================
About Layouts, Panels
=====================

If you have a large project with lots of views and templates,
you most likely have a lot of repetition. The header is the same,
the footer is the same. A lot of CSS/JS is pulled in, etc.

Lots of template systems have ways to share templating between
templates. But how do you get the data into the master template? You
can put it in the view and pass it in, but then it is hard to know what
parts belong to the view versus the main template. Then there's
testing, overriding, cases where you have multiple main templates.

Wouldn't it be nice to have a formal concept called "Layout" that
gained many of the benefits of Pyramid machinery like views?

This section introduces the concepts of :term:`layout` and "panel".

About Layouts
=============

Most projects have a global look-and-feel and each view plugs into it.
In ZPT-based systems, this is usually done with a main template that
uses METAL to wrap each view's template.

Having the template, though, isn't enough. The template usually has
logic in it and needs data. Usually each view had to pass in
that data. Later, Pyramid's
:ref:`renderer globals <pyramid:beforerender_event>`
provided an elegant
facility for always having certain data available in all renderings.

In Pyramid Layout, these ideas are brought together and given a name:
:term:`layout`. A layout is a combination of templating and logic to which a
view template can point. With Pyramid Layout, :term:`layout` becomes a
first-class citizen with helper config machinery and defined plug points.

In more complex projects, different parts of the same site need different
layouts. Pyramid Layout provides a way for managing the use of different
layouts in different places in your application.

About Panels
============

In your project you might have a number of layouts and certainly many
view templates. Reuse is probably needed for little boxes on the
screen. Or, if you are using someone else's layout, you might want to
change one small part without forking the entire template.

In ZPT, macros provide this functionality. That is, re-usable snippets of
templating with a marginal amount of overidability. Like main templates,
though, they also have logic and data that need to be schlepped into the
template.

Pyramid Layout addresses these re-usable snippets with panels. A :term:`panel`
is a box on the screen driven by templating and logic. You make panels,
register them, and you can then use them in your view templates or :term:`main
templates <main template>`.

Moreover, making and using them is a very Pythonic, Pyramid-like process. For
example, you call your :term:`panel` as a normal Python callable and can pass
it arguments.  Registration of panels, like :term:`layouts <layout>`, is very
similar to registration of views in Pyramid.
