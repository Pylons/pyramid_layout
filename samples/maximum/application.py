import os

from bottlecap.layouts.popper.layout import PopperLayout

from paste.httpserver import serve
from pyramid.config import Configurator


class CustomLayout(PopperLayout):

    @property
    def global_nav_menus(self):
        return [
            dict(title="Item 1", selected="selected"),
            dict(title="Item 2", selected=None),
            dict(title="Item 3", selected=None),
            dict(title="Item 4", selected=None),
            dict(title="Item 5", selected=None)]


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
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    import sys
    folder = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(folder)
    app = main()
    serve(app, host='0.0.0.0')
