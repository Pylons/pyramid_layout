""" Override the data for the global-nav panel
"""

from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('bottlecap')
    config.scan('example.views')
    config.scan('example.panels')
    return config.make_wsgi_app()

