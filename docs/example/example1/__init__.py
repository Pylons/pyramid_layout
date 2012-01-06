""" This is a simple Pyramid app, no Bottlecap """

from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.scan('example.views')
    return config.make_wsgi_app()

