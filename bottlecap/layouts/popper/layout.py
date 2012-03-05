import json

from pyramid.decorator import reify
from pyramid.settings import asbool
from bottlecap.layout import layout_config


@layout_config(name='anonymous', template='templates/anonymous_layout.pt')
@layout_config(template='templates/popper_layout.pt')
class PopperLayout(object):

    # Some configurable options that can be overriden in a view
    project_name = 'Popper Sample'
    section_title = 'Section Title'
    page_title = 'Page Title'
    section_style = 'full'
    extra_css = ()
    extra_js = ()

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.app_url = request.application_url
        self.context_url = request.resource_url(context)
        self.portlets = []

    @reify
    def devmode(self):
        """Let templates know if we are in devmode, for comments """

        sn = 'bottlecap.devmode'
        dm = self.request.registry.settings.get(sn, "false")
        return dm == "true"

    @reify
    def use_css_pie(self):
        sn = 'bottlecap.use_css_pie'
        return asbool(self.request.registry.settings.get(sn, False))

    def add_portlet(self, name, *args, **kw):
        self.portlets.append((name, args, kw))

    # --
    # Head data for urls
    # and page globals for the client
    #
    # The static panel data below is temporary.
    # The microtemplates and the pushdown data handling
    # has already been moved out from here, and not coming back.
    # --

    def popper_static(self, fname):
        return self.request.static_url(
            'bottlecap.layouts.popper:static/%s' % fname)

    def js_static(self, fname):
        return self.request.static_url('jslibs:/%s' % fname)

    @apply
    def show_sidebar():
        def getter(self):
            return bool(self.portlets)
        def setter(self, value):
            # allow manual override
            self.__dict__['show_sidebar'] = value
        return property(getter, setter)

    @property
    def head_data(self):
        if getattr(self, '_head_data', None) is None:
            self._head_data = {
                'app_url': self.app_url,
                'context_url': self.context_url,

                # XXX this does not belong here, but for now
                # we generate the data for some panels here.
                # The pushdowns are already moved out from this place.
                'panel_data': {
                    'tagbox': {
                        'records': [
                            {
                                'count': 2,
                                'snippet': 'nondeleteable',
                                'tag': 'flyers'
                                },
                            {
                                'count': 2,
                                'snippet': 'nondeleteable',
                                'tag': 'park'
                                },
                            {
                                'count': 2,
                                'snippet': 'nondeleteable',
                                'tag': 'volunteer'
                                },
                            {
                                'count': 2,
                                'snippet': '',
                                'tag': 'un'
                                },
                            {
                                'count': 2,
                                'snippet': 'nondeleteable',
                                'tag': 'foreign_policy'
                                },
                            {
                                'count': 1,
                                'snippet': 'nondeleteable',
                                'tag': 'unsaid'
                                },
                            {
                                'count': 2,
                                'snippet': 'nondeleteable',
                                'tag': 'advocacy'
                                },
                            {
                                'count': 2,
                                'snippet': '',
                                'tag': 'zimbabwe'
                                },
                            {
                                'count': 2,
                                'snippet': 'nondeleteable',
                                'tag': 'aryeh_neier'
                                },
                        ],
                        'docid': -1352878729,
                        },
                    },
                }
        return self._head_data

    @property
    def head_data_json(self):
        return json.dumps(self.head_data)

    def use_microtemplates(self, names):
        self._used_microtemplate_names = names
        self._microtemplates = None
        # update head data with it
        self.head_data['microtemplates'] = self.microtemplates

    @property
    def microtemplates(self):
        """Render the whole microtemplates dictionary"""
        if getattr(self, '_microtemplates', None) is None:
            self._microtemplates = get_microtemplates(directory=_microtemplates,
                names=getattr(self, '_used_microtemplate_names', ()))
        return self._microtemplates


# FIXME Use pkg_resources
import os

_here = os.path.dirname(__file__)
_microtemplates = os.path.join(_here, 'microtemplates')


def get_microtemplates(directory, names=None):

    templates = {}

    all_filenames = {}
    for _fn in os.listdir(directory):
        if _fn.endswith('.mustache'):
            name = _fn[:-9]
            fname = os.path.join(directory, _fn)
            all_filenames[name] = fname

    # XXX Names can be a list of templates that the page needs.
    # For now on, we ignore names and include all the templates we have.
    names = all_filenames.keys()

    for name in names:
        #try:
        fname = all_filenames[name]
        #except KeyError:
        #    raise "No such microtemplate %s" % name
        templates[name] = file(fname).read()

    return templates

