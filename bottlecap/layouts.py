from pyramid.decorator import reify
from pyramid.renderers import get_renderer
from pyramid.url import resource_url
from pyramid.url import static_url
from pyramid.view import view_config

class Layouts(object):

    @reify
    def community_layout(self):
        renderer = get_renderer("templates/community_layout.pt")
        return renderer.implementation().macros['layout']


    @reify
    def macros(self):
        renderer = get_renderer("templates/macros.pt")
        return renderer.implementation().macros

    @reify
    def profile_name(self):
        return "John Doe"

    @reify
    def context_url(self):
        return resource_url(self.context, self.request)

    @reify
    def app_url(self):
        return self.request.application_url

    @reify
    def bottlecap_static(self):
        return static_url('bottlecap:static/', self.request)

    @view_config(name='bottlecap.globalNav', renderer='templates/global_nav.pt')
    @view_config(name='bottlecap.search', renderer='templates/search.pt')
    @view_config(name='bottlecap.contextTools', renderer='templates/context_tools.pt')
    @view_config(name='bottlecap.personalTools', renderer='templates/personal_tools.pt')
    @view_config(name='bottlecap.actionsMenu', renderer='templates/actions_menu.pt')
    @view_config(name='bottlecap.columnone', renderer='templates/columnone.pt')
    def my_view(self):
        return {'profile_name': 'John Doe'}
