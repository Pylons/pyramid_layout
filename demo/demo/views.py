from pyramid.view import view_config

@view_config(route_name='home', renderer='demo:templates/layout.mako')
def my_view(request):
    return {'project':'demo'}
