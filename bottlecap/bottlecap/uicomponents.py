from pyramid.view import view_config


@view_config(name='bottlecap.globalnav', renderer='templates/globalnav.pt')
@view_config(name='bottlecap.search', renderer='templates/search.pt')
@view_config(name='bottlecap.contextTools', renderer='templates/context_tools.pt')
@view_config(name='bottlecap.personaltools', renderer='templates/personaltools.pt')
@view_config(name='bottlecap.actionsMenu', renderer='templates/actions_menu.pt')
def my_view(request):
    return {'profile_name': 'John Doe'}
