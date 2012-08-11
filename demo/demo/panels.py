from pyramid_layout.panel import panel_config


@panel_config(
    name='navbar',
    renderer='demo:templates/panels/navbar.mako'
    )
def navbar(context, request):
    return {}


@panel_config(
    name='hero',
    renderer='demo:templates/panels/hero.mako'
    )
def hero(context, request, title='Hello, world!'):
    return {'title': title}


@panel_config(
    name='heading-mako',
    renderer='demo:templates/panels/heading.mako'
    )
def heading_mako(context, request):
    return {'title': 'Heading Mako'}


@panel_config(
    name='heading-chameleon',
    renderer='demo:templates/panels/heading.pt'
    )
def heading_chameleon(context, request):
    return {'title': 'Heading Chameleon'}


@panel_config(
    name='heading-jinja2',
    renderer='demo:templates/panels/heading.jinja2'
    )
def heading_jija2(context, request):
    return {'title': 'Heading Jinja2'}


@panel_config(name='headings')
def headings(context, request):
    lm = request.layout_manager
    layout = lm.layout
    if layout.headings:
        return '\n'.join([lm.render_panel(name, *args, **kw)
             for name, args, kw in layout.headings])
    return ''
