Demo App With Pyramid Layout
============================

Let's see Pyramid Layout in action with the demo application it
provides in ``demo``.

Installation
============

Normal Pyramid stuff:

#. Make a virtualenv

#. ``env/bin/python demo/setup.py develop``

#. ``env/bin/pserve demo/development.ini``

#. Open ``http://0.0.0.0:6543/`` in a browser

#. Click on the ``Home Mako``, ``Home Chameleon``, and
   ``Home Jinja2`` links in the header to see views for that use each.

Now let's look at some of the code.

Registration
============

Pyramid Layout defines configuration directives and decorators you can
use in our project. We need those loaded into our code. The demo does
this in the ``etc/development.ini`` file:

.. literalinclude:: ../demo/development.ini
    :lines: 9-12
    :language: ini
    :linenos:


The ``development.ini`` entry point starts in ``demo/__init__.py``:

.. literalinclude:: ../demo/demo/__init__.py
    :language: python
    :linenos:

This is all Configurator action. We register a route for each view. We
then scan our ``demo/layouts.py``, ``demo/panels.py``, and
``demo/views.py`` for registrations.

Layout
======

Let's start with the big picture: the global look-and-feel via a layout:

.. literalinclude:: ../demo/demo/layouts.py
    :language: python
    :linenos:

The ``@layout_config`` decorator comes from Pyramid Layout and allows
us to define and register a "layout". In this case we've stacked 3
decorators, thus making 3 layouts, one for each template language.

