from bottlecap.panel import panel_config


@panel_config(name='popper.global_logo',
              renderer='templates/global_logo.pt')
def global_logo(context, request):
    return dict(
        logo_href=request.layout_manager.layout.site_title_link,
        logo_title=request.layout_manager.layout.site_title,
    )


@panel_config(name='popper.global_nav',
        renderer='templates/global_nav.pt')
def global_nav(context, request):
    nav_menu = [
        dict(title="Item 1", url='#', selected=None),
        dict(title="Item 2", url='#', selected="selected"),
        dict(title="Item 3", url='#', selected=None),
        dict(title="Item 4", url='#', selected=None),
        dict(title="Item 5", url='#', selected=None)]
    return {'nav_menu': nav_menu}


@panel_config(name='popper.personal_tools',
              renderer='templates/personal_tools.pt')
def personal_tools(context, request):
    return dict(profile_name="John Doe")


@panel_config(name='popper.search', renderer='templates/search.pt')
@panel_config(name='popper.context_tools',
              renderer='templates/context_tools.pt')
@panel_config(name='popper.column_one', renderer='templates/column_one.pt')
def generic_panel(context, request):
    return {}


@panel_config(name='popper.actions_menu', renderer='templates/actions_menu.pt')
def action_menu(context, request):
    return {'actions': [
        {'title': 'Add', 'subactions': [
            {'title': 'Page', 'url': '#'},
            {'title': 'Folder', 'url': '#'},
            {'title': 'File', 'url': '#'},
            {'title': 'Blog Entry', 'url': '#'}]},
        {'title': 'Edit', 'url': '#'},
        {'title': 'Delete', 'url': '#', 'confirm': 'Are you sure?'}
    ]}


@panel_config(name='popper.letter_box', renderer='templates/letter_box.pt')
def letter_box(context, request):
    letters = [{'name': chr(ch),
                'href': '#' if ch in (67, 69, 75) else None,
                'is_current': True if ch == 65 else False}
               for ch in xrange(ord('A'), ord('Z') + 1)]
    return {'letters': letters}
