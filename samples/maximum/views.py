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
        return {"project": "Some Project"}

    @view_config('sample.test_component',
            renderer="templates/test_component.pt")
    def test_component(self):
        return {}

    @view_config('sample.global_nav',
        renderer='sample:templates/global_nav.pt')
    def global_nav(self):
        return {}

    @view_config('bottlecap.column_one',
        renderer='sample:templates/column_one.pt')
    def column_one(self):
        return {}