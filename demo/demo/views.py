from pyramid.view import view_config

@view_config(
    route_name='home.mako',
    renderer='demo:templates/home.mako'
    )
@view_config(
    route_name='home.chameleon',
    renderer='demo:templates/home.pt',
    layout='chameleon'
    )
@view_config(
    route_name='home.jinja2',
    renderer='demo:templates/home.jinja2',
    layout='jinja2'
    )
def home(request):
    lm = request.layout_manager
    lm.layout.add_heading('heading-mako')
    lm.layout.add_heading('heading-chameleon')
    lm.layout.add_heading('heading-jinja2')
    return {}
