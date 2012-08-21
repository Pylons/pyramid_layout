Demo App With Pyramid Layout
============================

Let's see Pyramid Layout in action with the demo application provided
in ``demo``.

Installation
------------

Normal Pyramid stuff:

#. Make a virtualenv

#. ``env/bin/python demo/setup.py develop``

#. ``env/bin/pserve demo/development.ini``

#. Open ``http://0.0.0.0:6543/`` in a browser

#. Click on the ``Home Mako``, ``Home Chameleon``, and
   ``Home Jinja2`` links in the header to see views for that use each.

Now let's look at some of the code.

Registration
------------

Pyramid Layout defines configuration directives and decorators you can
use in your project. We need those loaded into our code. The demo does
this in the ``etc/development.ini`` file:

.. literalinclude:: ../demo/development.ini
    :lines: 9-12
    :language: ini


The ``development.ini`` entry point starts in ``demo/__init__.py``:

.. literalinclude:: ../demo/demo/__init__.py
    :language: python
    :linenos:

This is all Configurator action. We register a route for each view. We
then scan our ``demo/layouts.py``, ``demo/panels.py``, and
``demo/views.py`` for registrations.

Layout
------

Let's start with the big picture: the global look-and-feel via a :term:`layout`:

.. literalinclude:: ../demo/demo/layouts.py
    :language: python
    :linenos:

The ``@layout_config`` decorator comes from Pyramid Layout and allows
us to define and register a :term:`layout`. In this case we've stacked 3
decorators, thus making 3 layouts, one for each template language.

.. note::

    The first ``@layout_config`` doesn't have a ``name`` and is thus
    the layout that you will get if your view doesn't specifically
    choose which layout it wants.

Lines 21-24 illustrates the concept of keeping templates and the template
logic close together. All views need to show the ``project_title``.
It's part of the global look-and-feel :term:`main template`. So we put this
logic on the *layout*, in one place as part of the global contract,
rather than having each view supply that data/logic.

Let's next look at where this is used in the template for one of the
3 layouts. In this case, the Mako template at
``demo/templates/layouts/layout.mako``:

.. code-block:: mako

    <title>${layout.project_title}, from Pylons Project</title>

Here we see an important concept and some important magic: the template
has a top-level variable ``layout`` available. This is an instance of
your :term:`layout class`.

For the ZPT crowd, if you look at the master template in
``demo/templates/layouts/layout.pt``, you might notice something weird
at the top: there's no ``metal:define-macro``. Since Chameleon allows a
template to be a top-level macro, Pyramid Layout automatically binds
the entire template to the macro named ``main_template``.

How does your view know to use a :term:`layout`? Let's take a look.

Connecting Views to a Layout
----------------------------

Our demo app has a very simple set of views:

.. literalinclude:: ../demo/demo/views.py
    :language: python
    :linenos:

We again have one callable with 3 stacked decorators. The decorators
are all normal Pyramid ``@view_config`` stuff.

The second one points at a Chameleon template in
``demo/templates/home.pt``:

.. literalinclude:: ../demo/demo/templates/home.pt
    :language: html

The first line is the one that opts the template into the :term:`layout`. In
``home.jinja2`` that line looks like:

.. code-block:: jinja

  {% extends main_template %}

For both of these, ``main_template`` is inserted by Pyramid Layout,
via a Pyramid renderer global, into the template's global namespace.
After that, it's normal semantics for that template language.

Back to ``views.py``. The view function grabs the ``Layout Manager``,
which Pyramid Layout conveniently stashes on the request. The
``LayoutManager``'s primary job is getting/setting the current :term:`layout`.
Which, of course, we do in this function.

Our function then grabs the :term:`layout instance` and manipulates some state
that is needed in the global look and feel. This, of course, could have been
done in our ``AppLayout`` class, but in some cases, different views have
different values for the headings.

Re-Usable Snippets with Panels
------------------------------

Our :term:`main template` has something interesting in it:

.. literalinclude:: ../demo/demo/templates/layouts/layout.mako
    :lines: 27-49
    :emphasize-lines: 3,12
    :language: mako

Here we break our global layout into reusable parts via :term:`panels <panel>`.
Where do these come from? ``@panel_config`` decorators, as shown in
``panels.py``. For example, this:

.. code-block:: mako

  ${panel('navbar')}

...comes from this:

.. literalinclude:: ../demo/demo/panels.py
    :language: python
    :lines: 4-25

The ``@panel_config`` registered a panel under the name ``navbar``,
which our template could then use **or override**.

The ``home.mako`` view template has a more interesting panel:

.. code-block:: mako

  ${panel('hero', title='Mako')}

...which calls:

.. literalinclude:: ../demo/demo/panels.py
    :language: python
    :lines: 28-33
    :linenos:

This shows that a :term:`panel` can be parameterized and used in different
places in different ways.
