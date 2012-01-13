
def includeme(config):
    config.add_static_view('popper-static', 'bottlecap.layouts.popper:static')
    config.add_static_view('jslibs-static', 'jslibs:')
    config.scan('bottlecap.layouts.popper.layout')
    config.scan('bottlecap.layouts.popper.panels')
