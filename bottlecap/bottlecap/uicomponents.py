from pyramid.view import view_config


@view_config(name='bottlecap.topbar', renderer='templates/topbar.pt')
def my_view(request):
    return {'profile_name': 'My profile'}
