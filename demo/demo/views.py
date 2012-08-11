from pyramid.view import view_config

@view_config(
    route_name='home',
    renderer='demo:templates/home.mako'
    )
def home(request):
    layout = request.layout_manager.layout
    layout.add_heading('heading-mako')
    layout.add_heading('heading-chameleon')
    layout.add_heading('heading-jinja2')
    return {'project':'demo'}
