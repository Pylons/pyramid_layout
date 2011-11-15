from pyramid.view import view_config

from layouts import Layouts

class ProjectorViews(Layouts):
    def __init__(self, request):
        self.request = request

    @view_config(renderer="templates/blogpage_view.pt")
    def blogpage_view(self):
        return {"project": "Some Project"}