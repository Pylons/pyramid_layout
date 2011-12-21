from bottlecap.layout import layout_config
from pyramid.decorator import reify


@layout_config(template='templates/popper_layout.pt')
class PopperLayout(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.context_url = request.resource_url(context)
        self.static_url = request.static_url('bottlecap.layouts.popper:static/')

    @reify
    def global_nav_menus(self):
        return [
            dict(title="Item 1", selected=None),
            dict(title="Item 2", selected="selected"),
            dict(title="Item 3", selected=None),
            dict(title="Item 4", selected=None),
            dict(title="Item 5", selected=None)]
