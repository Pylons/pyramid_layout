=========================
Site Management With Jove
=========================

Deploying your Pyramid app means confronting quite a number of pain
points.  Sure, WSGI is a standard for apps, but where do I plug in
my app and manage it?  What about other apps I might want to deploy
on the same system?

With pdq's cloud service, many of these facilities are setup up, ready
to go.  The facilities, and their configuration, is part of Jove, pdq's
"site manager".

Goals
=====

- Allow one Python process to run multiple, autonomous WSGI apps

- Provide clear (conceptual and implementation) places to put services
  provided by pdq, or overriden in a particular app/site

- Ultimately, a Web UI that allows add/edit/remove/manage on all
  sites/apps you have available in a pdq cloud

What is a Site?
===============

A site is a WSGI app that has whatever else is expected from pdq.  This
might mean, some sort of introspection for a GUI that manages stuff you
are running somewhere.

What is a Site Manager?
=======================

Each WSGI app, aka site, runs in a Python process with zero or more
other apps.  This thing that sits above each WSGI app houses some of
the services provided by pdq.  Thus, that thing is the Site Manager.

In most cases, the Site Manager will have the following:

- The Python process

  - With one Unix user

  - With one PG user

  - One Supervisor

  - One cron
- A logical unit across multiple cores/machines, meaning, your
  "Site Manager" might physically be 8 Python processes on 4 VMs.

- Manages multiple sites

  - Add/edit/remove WSGI apps, aka "sites"

  - Perhaps with a GUI, perhaps from command line, perhaps both

- Might provide some services that are shared across all sites

  - Admin-level users that exist in all sites

  - Parts of the WSGI pipeline

- Might provide services most sites will use, but not all

  - RelStorage connection

  - Transaction manager

  - Users

  - Catalog + pgtextindex

  - Repository

The "Site" might have:

- A WSGI app with extra stuff to plugin to Jove

  - Provided via entry point

  - Settings as Colander schema to allow CRUD via Site Manager GUI

- In some cases, different RelStorage connection, pgtextindex, etc.

- Middleware
