from pyramid.decorator import reify
from pyramid.renderers import get_renderer
from pyramid.url import resource_url
from pyramid.url import static_url
from pyramid.view import render_view


class LayoutManager(object):

    layouts = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.layouts = {}
        self.layouts['site'] = "gumball:/templates/site_layout.pt"

    def __getitem__(self, key):
        value = self.layouts[key]
        renderer = get_renderer(value)
        macro = renderer.implementation().macros[key]
        return macro

    def component(self, name):
        return render_view(self.context, self.request, name)

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
