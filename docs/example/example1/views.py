from pyramid.view import view_config

class ExampleViews(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(renderer="templates/index.pt")
    def index_view(self):
        """ Default View """

        return dict(project="Example Project 1")

