from bottlecap.panel import panel_config

template_dir = 'bottlecap:layouts/popper/templates'

@panel_config(name='popper.global_nav',
              renderer=template_dir + '/global_nav.pt')
def global_nav(context, request):
    nav_menu = [
        dict(title="Projects", url='/', selected="selected"),
        dict(title="Customers", url='/communities', selected=None),
        ]
    return {'nav_menu': nav_menu}
