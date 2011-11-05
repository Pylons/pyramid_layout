from pyramid.view import view_config

from layouts2 import Layouts

class ProjectorViews(Layouts):
    def __init__(self, request):
        self.request = request

    @view_config(renderer="templates/blogpage_view.pt",
                 name="blogentry_view")
    def blogpage_view(self):
        return {"project": "Some Project"}