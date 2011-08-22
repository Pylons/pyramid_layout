================
Tour of Packages
================

pdq is an assembly of separately-managed batteries.  For each need,
pdq has an opinion and a single choice.

==================  =====================   ======================
Facility            Package                 Details
==================  =====================   ======================
Language            Python 2.7
Web Framework       Pyramid 1.1
Templating          chameleon1
Storage             RelStorage+PG
Forms               Deform
Nice Forms          Balazs/Simons thing
Schemas             Colander
Content Types       Limone                  :doc:`content-types`
Site Management     Jove                    :doc:`site-management`
Packaging           buildout
Packaging           Private index
Cataloging          repoze.catalog
Text indexing       repoze.pgtextindex
DVCS                Git/GitHub
Tagging             KARL's tagging
Workflow            repoze.workflow
Mailin		    repoze.postoffice
Configuration       Paste/Pyramid .ini
Migration           repoze.evolution
Versioning          Shane's thing
Users               Rossi's thing
Security            Pyramid ACLs
JS Libraries        Pylons jslibs           :doc:`jslibs`
Theming             jQuery UI Themeroller
Documentation       Sphinx/readthedocs
Scaffolding         Paster Templates
Functional Testing  WebTest
CI                  Jenkins at Pylons
Composing UIs       SiteLayouts             :doc:`layouts`
Admin UI            Bottlecap
==================  =====================   ======================

Other points related to platform:

- Layouts and Bottlecap
- Panels and PanelButtons
- i18n
- Base content (Document, File, Image) and core schemas
- Logging

Other points related to deployment:

- VMs at hosting partner, failover
- nginx/uWSGI and loadbalancing
- Monitoring
- Staging
- Mailin
