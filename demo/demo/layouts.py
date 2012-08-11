from pyramid_layout.layout import layout_config


@layout_config(template='demo:templates/layouts/layout.mako')
@layout_config(
    name='chameleon',
    template='demo:templates/layouts/layout.pt'
    )
@layout_config(
    name='jinja2',
    template='demo:templates/layouts/layout.jinja2'
    )
class AppLayout(object):
    project_title = 'Pyramid Layout App!'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.home_url = request.application_url
        self.headings = []

    def add_heading(self, name, *args, **kw):
        self.headings.append((name, args, kw))
