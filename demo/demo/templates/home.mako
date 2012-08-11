<%inherit file="${context['main_template'].uri}"/>

<!-- Main hero unit for a primary marketing message or call to action -->
${panel('hero', title='Pyramid Layout!')}

<!-- Example row of columns -->
<div class="row">
  ${panel('heading-mako')}
  ${panel('heading-chameleon')}
  ${panel('heading-jinja2')}
</div>