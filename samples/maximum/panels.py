from bottlecap.panel import panel_config

@panel_config(name='popper.global_nav',
              renderer='templates/global_nav.pt')
def global_nav(context, request):
    nav_menu = [
        dict(title="Intranet", url='/', selected=None),
        dict(title="Communities", url='/communities', selected=None),
        dict(title="People", url='/peopleosf', selected=None),
        dict(title="Calendar", url='#', selected='selected'),
        dict(title="Feed", url='#', selected=None)]
    return {'nav_menu': nav_menu}
