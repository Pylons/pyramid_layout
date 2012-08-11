from pyramid_layout.panel import panel_config


@panel_config(
    name='hero',
    renderer='demo:templates/panels/hero.mako')
def hero(context, request, title='Hello, world!'):
    return {'title': title}


