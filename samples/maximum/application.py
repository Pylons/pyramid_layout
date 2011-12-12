
from paste.httpserver import serve
from pyramid.config import Configurator

from bottlecap.layout import LayoutManager


class MyLayoutManager(LayoutManager):

    @property
    def global_nav_menus(self):
        menu_items = [
            dict(title="Item 1", selected='selected'),
            dict(title="Item 2", selected=None),
            dict(title="Item 3", selected=None),
            dict(title="Item 4", selected=None),
            dict(title="Item 5", selected=None),
            ]
        return menu_items


def main():
    config = Configurator()
    config.registry.settings['reload_templates'] = True
    config.include('bottlecap')
    config.add_bc_layout({
        'site': 'sample:templates/site_layout.pt'
        })
    config.add_bc_layoutmanager_factory(MyLayoutManager)
    config.scan('views')
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    import os
    import sys
    folder = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(folder)
    app = main()
    serve(app, host='0.0.0.0')
