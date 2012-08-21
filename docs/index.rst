=========================================
Pyramid Layout: Composable UX for Pyramid
=========================================

Making an attractive, efficient user-experience (UX) is hard. Pyramid Layout
provides a layout-based approach to building your global look-and-feel
then re-using it across your site. You can then manage your global UX
:term:`layout` as a unit, just like models, views, static resources, and
other parts of Pyramid.

If you are OCD, and want the same ways to organize and override your UX
that you get in your Python code, this :term:`layout` approach is your
cup of tea.

Approach
========

- Make one (or more) :term:`layout` objects of template and template logic

- Do useful things with this unit of layout: registration,
  dynamic association with a view, pluggability via Pyramid overrides,
  testing in isolation

- Layouts can share lightweight units called :term:`panels <panel>` which are
  objects of template and code, sharing the same useful things

- Use of any of the common Pyramid templating engines (Chameleon ZPT, Mako,
  Jinja2) is tested and supported with examples.

Contents
========

.. toctree::
    :maxdepth: 2

    about
    layouts
    demo
    api
    glossary

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`

