from pyramid_layout.layout import layout_config


@layout_config(template='demo:templates/layout.mako')
class AppLayout(object):
    project_title = 'Pyramid Layout App!'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.home_url = request.application_url
