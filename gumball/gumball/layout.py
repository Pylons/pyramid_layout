from pyramid.decorator import reify
from pyramid.renderers import get_renderer
from pyramid.url import resource_url
from pyramid.url import static_url


class LayoutManager(object):

    layout_templates = None
    uicomponents_template = "gumball:/templates/uicomponents.pt"

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.layout_templates = {}
        self.layout_templates['site'] = "gumball:/templates/site_layout.pt"

    def __getitem__(self, key):
        renderer = get_renderer(self.layout_templates[key])
        macros = renderer.implementation().macros[key]
        return macros

    @reify
    def uicomponents(self):
        renderer = get_renderer(self.uicomponents_template)
        macros = renderer.implementation().macros
        return macros

    @reify
    def context_url(self):
        return resource_url(self.context, self.request)

    @reify
    def app_url(self):
        return self.request.application_url

    @reify
    def gumball_static(self):
        return static_url('gumball:static/', self.request)

    @reify
    def jslibs_static(self):
        return static_url('jslibs:resources/', self.request)

    @reify
    def deform_static(self):
        return static_url('deform:static/', self.request)


def inject_static(config):
    # TODO sure would be nice if I could make a Configurator instance
    # and do this myself

    # config.add_static_view('static-jslibs', 'jslibs:resources/',
    #                        cache_max_age=86400)
    config.add_static_view('static', 'gumball:static/',
                           cache_max_age=86400)
