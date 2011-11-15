from pyramid.view import view_config


@view_config(renderer="bottlecap:templates/index.pt")
def index_view(request):
    return {"project": "Some Project"}
