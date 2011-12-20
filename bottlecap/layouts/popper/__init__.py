
def includeme(config):
    config.add_layout('templates/popper_layout.pt',       # default layout
                      globals_factory=globals_factory)
    config.add_static_view('popper-static', 'bottlecap.layouts.popper:static')
    config.scan('bottlecap.layouts.popper.panels')


def globals_factory(context, request):
    return {
        'global_nav_menus': [
            dict(title="Item 1", selected=None),
            dict(title="Item 2", selected="selected"),
            dict(title="Item 3", selected=None),
            dict(title="Item 4", selected=None),
            dict(title="Item 5", selected=None)],
        'context_url': request.resource_url(context),
        'static_url': request.static_url('bottlecap.layouts.popper:static/')}
