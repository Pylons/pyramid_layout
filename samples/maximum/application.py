import os

from bottlecap.layouts.popper.layout import PopperLayout

from paste.httpserver import serve
from pyramid.config import Configurator


class CustomLayout(PopperLayout):
    """
    Pretend like we added something custom and useful here.
    """


def main():
    config = Configurator()
    config.registry.settings['reload_templates'] = True
    config.include('bottlecap')
    # Since we're not running in a package, we need an absolute path
    site_template = os.path.abspath('templates/site_layout.pt')
    popper_template = 'bottlecap.layouts.popper:templates/popper_layout.pt'
    config.add_layout(CustomLayout, site_template, 'site')
    config.add_layout(CustomLayout, popper_template)

    config.scan('views')
    config.scan('panels')
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    import sys
    folder = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(folder)
    app = main()
    serve(app, host='0.0.0.0')
