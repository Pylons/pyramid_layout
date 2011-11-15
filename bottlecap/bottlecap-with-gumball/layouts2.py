from pyramid.renderers import get_renderer
from pyramid.decorator import reify

class Layouts(object):

    @reify
    def community_layout(self):
        renderer = get_renderer("templates/community_layout.pt")
        return renderer.implementation().macros['layout']

    @reify
    def company_name(self):
        return 999
