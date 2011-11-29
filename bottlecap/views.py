from pyramid.view import view_config


# Component Views
@view_config(name='bottlecap.personal_tools',
        renderer='bottlecap:templates/personal_tools.pt')
def personal_tools(context, request):
    return dict(profile_name="John Doe")

@view_config(name='bottlecap.global_nav',
        renderer='bottlecap:templates/global_nav.pt')
def global_nav(context, request):
    return {}

@view_config(name='bottlecap.search',
        renderer='bottlecap:templates/search.pt')
def search(context, request):
    return {}

@view_config(name='bottlecap.context_tools',
        renderer='bottlecap:templates/context_tools.pt')
def context_tools(context, request):
    return {}

@view_config(name='bottlecap.actions_menu',
        renderer='bottlecap:templates/actions_menu.pt')
def actions_menu(context, request):
    return {}

@view_config(name='bottlecap.column_one',
        renderer='bottlecap:templates/column_one.pt')
def column_one(context, request):
    return {}
