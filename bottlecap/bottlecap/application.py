from paste.httpserver import serve
from pyramid.config import Configurator


def main():
    config = Configurator()
    config.registry.settings['reload_assets'] = True
    config.registry.settings['reload_resources'] = True
    config.registry.settings['reload_templates'] = True
    config.scan("views")
    config.add_static_view('bc-static', 'bottlecap:static/',
                           cache_max_age=86400)
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main()
    serve(app, host='0.0.0.0')
