#
# This is the magic chant you have to do in your view code, unless
# we find a way to eliminate it
#
from pyramid.events import subscriber
from pyramid.events import BeforeRender

from gumball.layout import LayoutManager


@subscriber(BeforeRender)
def add_renderer_globals(event):
    request, context = event['request'], event['context']
    event['layout'] = LayoutManager(context, request)
