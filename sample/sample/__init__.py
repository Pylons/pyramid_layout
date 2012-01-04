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

    config.scan('.panels')
    config.scan('.views')
    return config.make_wsgi_app()

