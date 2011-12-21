
def includeme(config):
    # Define without a name, context or containment--default layout
    config.add_layout('bottlecap.layouts.popper.layout.PopperLayout',
                      'templates/popper_layout.pt')
    config.add_static_view('popper-static', 'bottlecap.layouts.popper:static')
    config.scan('bottlecap.layouts.popper.panels')
