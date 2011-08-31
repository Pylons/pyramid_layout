from paste.httpserver import serve
from pyramid.config import Configurator

from gumball.layout import inject_static


def main():
    config = Configurator()
    config.scan("gumball.sample")
    config.include(inject_static)
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main()
    serve(app, host='0.0.0.0')
