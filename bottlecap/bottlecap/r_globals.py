#
# This is the magic chant you have to do in your view code, unless
# we find a way to eliminate it
#
from gumball.layout import LayoutManager
from pyramid.events import BeforeRender
from pyramid.events import subscriber


@subscriber(BeforeRender)
def add_renderer_globals(event):
    request, context = event['request'], event['context']
    layout = LayoutManager(context, request)
    layout.layout_templates['site'] = "bottlecap:/templates/site_layout.pt"
    layout.uicomponents_template = "bottlecap:/templates/uicomponents.pt"
    event['layout'] = layout
    event['app'] = dict(app_static="/bc-static/")
