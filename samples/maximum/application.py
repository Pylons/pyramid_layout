
from paste.httpserver import serve
from pyramid.config import Configurator

from bottlecap.layout import LayoutManager


class MyLayoutManager(LayoutManager):

    @property
    def global_nav_menus(self):
        menu_items = [
            dict(title="Intranet", selected=None),
            dict(title="Communities", selected='selected'),
            dict(title="People", selected=None),
            dict(title="Calendar", selected=None),
            dict(title="Feed", selected=None),
            ]
        return menu_items


def main():
    config = Configurator()
    config.registry.settings['reload_templates'] = True
    config.include('bottlecap')
    config.add_bc_layout({
        'site': 'templates/site_layout.pt'
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
