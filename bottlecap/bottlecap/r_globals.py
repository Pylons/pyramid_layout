#
# This is the magic chant you have to do in your view code, unless
# we find a way to eliminate it
#
from pyramid.events import subscriber
from pyramid.events import BeforeRender

from gumball.layout import LayoutManager

@subscriber(BeforeRender)
def add_renderer_globals(event):
    system = event._system
    request, context = system['request'], system['context']
    layout = LayoutManager(context, request)
    layout.layout_template = "bottlecap:/templates/site_layout.pt"
    event['layout'] = layout
    event['app'] = dict(app_static="/bc-static/")
