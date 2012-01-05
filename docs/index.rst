.. Bottlecap documentation master file, created by
   sphinx-quickstart on Wed Jan  4 16:41:52 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================================
Bottlecap: Composable, Attractive UX for Pyramid
================================================

Making an attractive, efficient user-experience (UX) is hard. Bottlecap
provides a layout-based approach to building your global look-and-feel
then re-using it across your site. You can then manage your global UX
"layout" as a unit, just like models, views, static resources, and
other parts of Pyramid.

Even better, Bottlecap ships an attractive, pluggable, well-maintained
example layout called Popper which you can plug into your Pyramid app
as a starting point.

Benefits
========

- If you suck at prettiness, use Popper as your starting point until
  you need your own UX

- Work on your global look-and-feel (aka theme, aka skin,
  aka main template, aka o-wrap) as a distinct artifact.

- Allow per-view, or per-project customization points using familiar
  Pyramid idioms

.. note::

    Bottlecap is aimed at ZPT-based applications. You can write panels
    in any templating system, as they simply have to return strings. It
    is possible that you can do all of Bottlecap in another
    Pyramid-supported templating system, but that is untested.

Contents
========

.. toctree::
    :maxdepth: 2

    about
    howitworks
    usingpopper
    usinglayoutspanels
    faq

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

