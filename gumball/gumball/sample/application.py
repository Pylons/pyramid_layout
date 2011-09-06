from paste.httpserver import serve
from pyramid.config import Configurator


def main():
    config = Configurator()
    config.scan("gumball.sample")
    from gumball.sample import layout
    config.include(layout.configure)
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main()
    serve(app, host='0.0.0.0')
