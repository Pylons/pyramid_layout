from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home.mako', '/')
    config.add_route('home.chameleon', '/chameleon')
    config.add_route('home.jinja2', '/jinja2')
    config.scan('.layouts')
    config.scan('.panels')
    config.scan('.views')
    return config.make_wsgi_app()
