=======================
Motivation: Terminology
=======================

Before we start, we need to define some common terminology. While the web
itself is rather old, the processes and ways to build web applications are
still rather in its infancy. While web browsers support some UI controls, they
are build for a page or document centric presentation model - not as an
application platform. We'll use a terminology that is similar to the one used
to describe non-web applications using classical GUI frameworks.

On a technical level a web application presents itself to the user via URL's
mapped to HTML pages. In an application these HTML pages will share a common
visual theme and general structure.

The visual :term:`theme` consists of graphical appearance rules, typography and
common graphical elements like icons.

.. note::
    In the CMF/Plone world this used to be called a skin.

Most pages will share a general structure, like the same header or footer,
global navigation elements or a number of columns. We call this structure a
:term:`layout`, as it refers to how elements or laid out on the screen.

Generally there's one overall layout that's used by all pages. We call this the
:term:`site layout`. Some subsection or functional areas of the site might have
a different structure, so there can be more than one layout.

The spatial arrangement of elements inside a layout is implemented via CSS and
can use a :term:`grid layout` or column layout or combinations thereof.

In addition to the overall layout, there's also further common elements which
might be used on all or just some pages. Examples are a search box, a sidebar,
a footer containing contact information or a sub-navigation. We will call these
types of elements :term:`UI components`.

UI components generally consist of some HTML output and potentially some
associated JavaScript. UI components can either be purely presentational like
a footer text, implement some UI controls like a search box or have grouping
purposes like a dialog or a panel. Any UI component might have some CSS that
the theme should incorporate for the UI component to be presented correctly.

.. note::
    In the Plone world tiles, viewlets and portlets are examples of UI
    components.

If a UI component implements some UI control, it is often called a
:term:`widget`. Sometimes the term widget is reserved for those controls, which
are part of an HTML form, though this is technical distinction that's not
apparent for the user.

There's various types of grouping UI components, like dialogs, panels and
windows, which can in turn contain further UI components.

.. note::
    In the Plone Deco world, the term panel has a special meaning and is the
    only grouping element that can contain multiple UI components (tiles).

In order to access the layout or any of the UI components, an application has
one :term:`layout manager`, which has API's to get to these components.

UI components and layouts are implemented using views or templates. In order to
avoid confusion we only use the term template for Chameleon page templates.

A layout defines various regions, which will contain page specific UI
components. We expose those regions as Chameleon METAL macros.
