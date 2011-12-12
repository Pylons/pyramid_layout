from paste.httpserver import serve
from pyramid.config import Configurator

def main():
    config = Configurator()
    config.registry.settings['reload_templates'] = True

    # This include injects a Layout Manager instance into the
    # renderer globals as the variable lm
    config.include('bottlecap')

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
