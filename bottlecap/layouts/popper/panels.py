from bottlecap.panel import panel_config


@panel_config(name='popper.personal_tools',
        renderer='templates/personal_tools.pt')
def personal_tools(context, request):
    return dict(profile_name="John Doe")

@panel_config(name='popper.global_nav',
        renderer='templates/global_nav.pt')
def global_nav(context, request):
    return {}

@panel_config(name='popper.search',
        renderer='templates/search.pt')
def search(context, request):
    return {}

@panel_config(name='popper.context_tools',
        renderer='templates/context_tools.pt')
def context_tools(context, request):
    return {}

@panel_config(name='popper.actions_menu',
        renderer='templates/actions_menu.pt')
def actions_menu(context, request):
    return {}

@panel_config(name='popper.column_one',
        renderer='templates/column_one.pt')
def column_one(context, request):
    return {}
