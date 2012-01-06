""" Add the Popper layout from Bottlecap, nothing more
"""

from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('bottlecap')
    config.scan('example.views')
    return config.make_wsgi_app()

