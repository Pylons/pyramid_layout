=========
Bottlecap
=========

When building a new Pyramid application, you might want an attractive
starting point for your UI. Later, as you need a custom UX, you might
want a system for organizing your global UX and shared templating into
layouts and panels.

Bottlecap serves that purpose.

- Inject Bottlecap into your application

- Point your ZPTs at Bottlecap's Popper layout

- Configure, override and extend using Pyramid machinery

- Later, make and register your own layouts and panels

Quick Start
===========

You can see Bottlecap added to a sample Pyramid app that ships in
Bottlecap:

#. Make a virtualenv as usual.

#. ``git clone git@github.com:pauleveritt/pyramid_bottlecap.git``

#. ``cd pyramid_bottlecap``

#. ``/virtualenv/bin/python setup.py develop``

#. ``cd sample``

#. ``/virtualenv/bin/python setup.py develop``

#. ``/virtualenv/bin/pserve development.ini --reload``

#. Open ``http://localhost:6543`` in a browser.

Bottlecap will now be running on port 6543. To run the WebTest tests
on the templates in the sample app::

  $ ``/virtualenv/bin/nosetests``

More information is available in the ``docs`` directory.
