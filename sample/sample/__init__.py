from pyramid.config import Configurator

from bottlecap.layouts.popper.layout import PopperLayout


class CustomLayout(PopperLayout):
    """
    Pretend like we added something custom and useful here.
    """


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('bottlecap')
    alternative_template = 'sample:templates/alternative_layout.pt'
    config.add_layout(CustomLayout, alternative_template,
                      'alternative')
    popper_template = 'bottlecap.layouts.popper:templates/popper_layout.pt'
    config.add_layout(CustomLayout, popper_template)
    config.add_static_view('static', 'sample:static')
    # favicon override
    config.override_asset(
             to_override='bottlecap.layouts.popper:static/img/favicon.ico',
             override_with='sample:static/img/favicon.ico')
    config.scan('sample.panels')
    config.scan('sample.views')
    return config.make_wsgi_app()

