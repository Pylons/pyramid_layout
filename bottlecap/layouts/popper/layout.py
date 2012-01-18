import json

from pyramid.decorator import reify
from pyramid.settings import asbool
from bottlecap.layout import layout_config


@layout_config(template='templates/popper_layout.pt')
class PopperLayout(object):

    # Some configurable options that can be overriden in a view
    show_sidebar = True
    section_style = 'full'
    project_name = 'Popper Sample'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.app_url = request.application_url
        self.context_url = request.resource_url(context)
        self.static_url = request.static_url('bottlecap.layouts.popper:static/')
        self.jslibs_static_url = request.static_url('jslibs:/')

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

    # --
    # Head data and microtemplates management
    # I've been told this is temporary.
    # --

    @property
    def head_data(self):
        if getattr(self, '_head_data', None) is None:
            self._head_data = {
                'app_url': self.app_url,
                'context_url': self.context_url,
                'microtemplates': self.microtemplates,
                # XXX this does not belong here, but for now
                # we generate the data for chatterpanel here.
                'panel_data': {
                    'chatter': {
                        'streams': [{
                            'class': 'your-stream',
                            'title': '@plonepaul (to you)',
                            'items': [{
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh...',
                                    'info': '(3 min ago, 2 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': '"At vero eos et accusamus et iusto odio dignissimos ducimus...',
                                    'info': '(4 min ago, 4 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod...',
                                    'info': '(5 min ago, 3 files)',
                                }],
                            }, {
                            'class': 'recent-friend',
                            'title': 'Recent Friend Chatter',
                            'items': [{
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh...',
                                    'info': '(3 min ago, 2 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'At vero eos et accusamus et iusto odio dignissimos ducimus...',
                                    'info': '(4 min ago, 4 files)',
                                }],
                            }],
                        },

                    'radar': {
                        'streams': [{
                            'class': 'stream1',
                            'title': 'Action',
                            'items': [{
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh...',
                                    'info': '(3 min ago, 2 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': '"At vero eos et accusamus et iusto odio dignissimos ducimus...',
                                    'info': '(4 min ago, 4 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod...',
                                    'info': '(5 min ago, 3 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod...',
                                    'info': '(5 min ago, 3 files)',
                                }],
                            }, {
                            'class': 'stream2',
                            'title': '@plonepaul (to you)',
                            'items': [{
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh...',
                                    'info': '(3 min ago, 2 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'At vero eos et accusamus et iusto odio dignissimos ducimus...',
                                    'info': '(4 min ago, 4 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod...',
                                    'info': '(5 min ago, 3 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod...',
                                    'info': '(5 min ago, 3 files)',
                                }],
                            }, {
                            'class': 'stream3',
                            'title': '@plonepaul (to you)',
                            'items': [{
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh...',
                                    'info': '(3 min ago, 2 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'At vero eos et accusamus et iusto odio dignissimos ducimus...',
                                    'info': '(4 min ago, 4 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod...',
                                    'info': '(5 min ago, 3 files)',
                                }, {
                                    'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                                    'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod...',
                                    'info': '(5 min ago, 3 files)',
                                }],
                            }],
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
            self._microtemplates = get_microtemplates(
                names=getattr(self, '_used_microtemplate_names', ()))
        return self._microtemplates


# FIXME Use pkg_resources
import os

_here = os.path.dirname(__file__)
_microtemplates = os.path.join(_here, 'microtemplates')


def get_microtemplates(names=None):

    templates = {}

    all_filenames = {}
    for _fn in os.listdir(_microtemplates):
        if _fn.endswith('.mustache'):
            name = _fn[:-9]
            fname = os.path.join(_microtemplates, _fn)
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

