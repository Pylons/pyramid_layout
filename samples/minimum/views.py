from pyramid.view import view_config


class HelloWorldView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(renderer="templates/index_view.pt")
    def index_view(self):
        return {"project": "HelloWorld Project"}
