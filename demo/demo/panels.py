from pyramid_layout.panel import panel_config


@panel_config(
    name='navbar',
    renderer='demo:templates/panels/navbar.mako')
def navbar(context, request):
    return {}


@panel_config(
    name='hero',
    renderer='demo:templates/panels/hero.mako')
def hero(context, request, title='Hello, world!'):
    return {'title': title}
