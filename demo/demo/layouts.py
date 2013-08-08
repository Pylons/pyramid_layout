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

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.home_url = request.application_url
        self.headings = []
        self.portlets = (Thing1(), Thing2(), LittleCat("A"))

    @property
    def project_title(self):
        return 'Pyramid Layout App!'

    def add_heading(self, name, *args, **kw):
        self.headings.append((name, args, kw))


class Thing1(object):
    title = "Thing 1"
    content = "I am Thing 1!"


class Thing2(object):
    title = "Thing 2"
    content = "I am Thing 2!"


class LittleCat(object):
    talent = "removing pink spots"

    def __init__(self, name):
        self.name = name
