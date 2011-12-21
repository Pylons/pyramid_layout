
def includeme(config):
    config.add_static_view('popper-static', 'bottlecap.layouts.popper:static')
    config.scan('bottlecap.layouts.popper.layout')
    config.scan('bottlecap.layouts.popper.panels')
