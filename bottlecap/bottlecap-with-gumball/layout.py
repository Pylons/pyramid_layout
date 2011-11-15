import gumball.layout
from pyramid.decorator import reify
from pyramid.events import BeforeRender
from pyramid.events import subscriber
from pyramid.url import static_url

LAYOUTS = {
    'site': 'bottlecap:/templates/site_layout.pt',
}


class LayoutManager(gumball.layout.LayoutManager):

    @reify
    def bottlecap_static(self):
        return static_url('bottlecap:static/', self.request)


@subscriber(BeforeRender)
def add_renderer_globals(event):
    request, context = event['request'], event['context']
    event['layout'] = LayoutManager(context, request, LAYOUTS)


def configure(config):
    config.include(gumball.layout.configure)
    config.add_static_view('bc-static', 'bottlecap:static/',
                           cache_max_age=86400)
