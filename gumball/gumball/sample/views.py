from pyramid.view import view_config

@view_config(renderer="gumball:sample/templates/index.pt")
def index_view(request):
    return {"project": "Some Project"}
