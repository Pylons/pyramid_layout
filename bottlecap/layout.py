#import types

from pyramid.decorator import reify
from pyramid.renderers import get_renderer
from pyramid.url import resource_url
from pyramid.url import static_url
from pyramid.view import render_view

from zope.interface import implements
from zope.interface import Interface

DEFAULT_LAYOUTS = {
    'community': 'bottlecap:/templates/community_layout.pt',
    }


class ILayoutManagerFactory(Interface):
    pass


class LayoutManager(object):
    implements(ILayoutManagerFactory)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.layouts = DEFAULT_LAYOUTS

    def _add_layout(self, layout):
        self.layouts.update(layout)

    def layout(self, name):
        value = self.layouts[name]
        renderer = get_renderer(value)
        macro = renderer.implementation()
        return macro

    def component(self, name):
        return Structure(render_view(self.context, self.request, name))

    @reify
    def context_url(self):
        return resource_url(self.context, self.request)

    @reify
    def app_url(self):
        return self.request.application_url

    @reify
    def bottlecap_static(self):
        return static_url('bottlecap:static/', self.request)

    @reify
    def global_nav_menus(self):
        # TODO we will need a way in sample/application (the custom
        # app) to reach over and grab lm instance to override
        menu_items = [
            dict(title="Intranet", selected=None),
            dict(title="Communities", selected="selected"),
            dict(title="People", selected=None),
            dict(title="Calendar", selected=None),
            dict(title="Explore", selected=None),
            ]
        return menu_items


class Structure(unicode):
    # Wrapping a string in this class avoids having to prefix the value
    # with `structure` in TAL

    def __html__(self):
        return self


def add_bc_layout(config, layout):
    settings = config.registry.settings
    bc = settings['bc']
    if isinstance(layout, dict):
        bc['layouts'] = layout


def add_bc_layoutmanager_factory(config, factory):
    factory = config.maybe_dotted(factory)
    config.registry.registerUtility(factory, ILayoutManagerFactory)

