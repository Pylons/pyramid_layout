from bottlecap.panel import panel_config
from pyramid.view import view_config


class SampleBlogView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(renderer="templates/blogpage_view.pt")
    def blogpage_view(self):
        return {"project": "Some Project"}

    @view_config('test', renderer="templates/testpage_view.pt")
    def testpage_view(self):
        self.request.layout_manager.use_layout('site')
        return {"project": "Some Project"}

    @panel_config('sample.test_panel', renderer="templates/test_panel.pt")
    def test_panel(self):
        return {}

    @panel_config('popper.global_nav', renderer='templates/global_nav.pt')
    def global_nav(self):
        nav_menu = [
            dict(title="Intranet", url='#', selected=None),
            dict(title="Communities", url='#', selected='selected'),
            dict(title="People", url='#', selected=None),
            dict(title="Calendar", url='#', selected=None),
            dict(title="Feed", url='#', selected=None)]
        return {'nav_menu': nav_menu}

    @panel_config('bottlecap.column_one', renderer='templates/column_one.pt')
    def column_one(self):
        return {}
