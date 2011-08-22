from pyramid.config import Configurator
from paste.httpserver import serve

from gumball.layout import inject_static

def main():
    config = Configurator()
    config.scan("bottlecap")
    config.include(inject_static)
    config.add_static_view('bc-static', 'bottlecap:static/',
                           cache_max_age=86400)
    app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    app = main()
    serve(app, host='0.0.0.0')
