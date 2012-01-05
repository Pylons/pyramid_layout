=========
Bottlecap
=========

When building a new Pyramid application, you might want an attractive
starting point for your UI. Bottlecap serves that purpose. Mix
Bottlecap into your Pyramid/ZPT application and use it until you get
your own UX in place.

- Inject Bottlecap into your application

- Point your ZPTs at one of Bottlecap's "layouts"

- Configure, override and extend using subclassing and view machinery

Quick Start
===========

You can see Bottlecap added to a simple sample Pyramid app that ships
in Bottlecap:

#. Make a virtualenv as usual.

#. ``cd pyramid_bottlecap``

#. ``path/to/virtualenv/bin/python setup.py develop``

#. ``cd sample``

#. ``path/to/virtualenv/bin/python setup.py develop``

#. ``path/to/virtualenv/bin/pserve development.ini --reload``

#. Open ``http://localhost:6543`` in a browser.

Bottlecap will now be running on port 6543. To run the WebTest tests
on the templates in the sample app:

$ ``path/to/virtualenv/bin/nosetests``

More information is available in the ``docs`` directory.
