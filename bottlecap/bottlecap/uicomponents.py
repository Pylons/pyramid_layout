from pyramid.view import view_config


@view_config(name='bottlecap.globalNav', renderer='templates/global_nav.pt')
@view_config(name='bottlecap.search', renderer='templates/search.pt')
@view_config(name='bottlecap.contextTools', renderer='templates/context_tools.pt')
@view_config(name='bottlecap.personalTools', renderer='templates/personal_tools.pt')
@view_config(name='bottlecap.actionsMenu', renderer='templates/actions_menu.pt')
@view_config(name='bottlecap.columnone', renderer='templates/columnone.pt')
def my_view(request):
    return {'profile_name': 'John Doe'}
