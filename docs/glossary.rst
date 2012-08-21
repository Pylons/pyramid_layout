.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   layout
     The basic unit of reusable look and feel, a layout consists of a 
     :term:`main template` and a :term:`layout class`.

   layout class
     A class registered with a layout that can be used as a place to consolidate
     API that is common to all or many templates across a project. 

   layout instance
     An instance of a :term:`layout class`.  For each view, a :term:`layout` is
     selected and that layout's :term:`layout class` is instantiated for the
     current :pyramid:term:`request` and :pyramid:term:`context` and made
     available to templates as the :pyramid:term:`renderer global <renderer
     globals>`, ``layout``.

   main template
     Also known as the `o-wrap` or `outer wrapper`, this is a template which
     contains HTML that is common to all views that share a particular layout.
     View templates are derived from the main template and inject their own 
     HTML into the HTML defined by the main template.

   panel
     A panel is a reusable component that defines the HTML for small piece of an
     entire page.  Panels are callables, like :pyramid:term:`views <view
     callable>`, and may either return an HTML string or use a
     :pyramid:term:`renderer` for generating HTML to embed in the page.
