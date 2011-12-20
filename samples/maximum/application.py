import os

from paste.httpserver import serve
from pyramid.config import Configurator


def globals_factory(context, request):
    return {
        'global_nav_menus': [
            dict(title="Item 1", selected='selected'),
            dict(title="Item 2", selected=None),
            dict(title="Item 3", selected=None),
            dict(title="Item 4", selected=None),
            dict(title="Item 5", selected=None)],
        'context_url': request.resource_url(context),
        'static_url': request.static_url('bottlecap.layouts.popper:static/')}


def main():
    config = Configurator()
    config.registry.settings['reload_templates'] = True
    config.include('bottlecap')
    # Since we're not running in a package, we need an absolute path
    layout = os.path.abspath('templates/site_layout.pt')
    config.add_layout(layout, 'site', globals_factory=globals_factory)

    # Redefine global layout from Popper to use our globals_factory
    config.add_layout('bottlecap.layouts.popper:templates/popper_layout.pt',
                      globals_factory=globals_factory)

    config.scan('views')
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    import sys
    folder = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(folder)
    app = main()
    serve(app, host='0.0.0.0')
