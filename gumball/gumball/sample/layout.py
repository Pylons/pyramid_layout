from gumball.layout import configure as gumball_configure
from gumball.layout import LayoutManager
from gumball.layout import LAYOUTS
from pyramid.events import subscriber
from pyramid.events import BeforeRender


@subscriber(BeforeRender)
def add_renderer_globals(event):
    request, context = event['request'], event['context']
    event['layout'] = LayoutManager(context, request, LAYOUTS)


def configure(config):
    config.include(gumball_configure)
