import json

from bottlecap.interfaces import IPanel
from pyramid.decorator import reify
from pyramid.renderers import get_renderer
from pyramid.url import resource_url
from pyramid.url import static_url

from zope.interface import implements
from zope.interface import Interface
from zope.interface import providedBy


from bottlecap.utils import get_microtemplates


DEFAULT_LAYOUTS = {
    'global': 'bottlecap:/templates/global_layout.pt',
    }


_marker = object()


class ILayoutManagerFactory(Interface):
    pass


class LayoutManager(object):
    implements(ILayoutManagerFactory)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.layouts = DEFAULT_LAYOUTS

    def _add_layout(self, layout):
        self.layouts.update(layout)

    def layout(self, name):
        value = self.layouts[name]
        renderer = get_renderer(value)
        macro = renderer.implementation()
        return macro

    def panel(self, name, *args, **kw):
        context = self.context
        request = self.request
        adapters = request.registry.adapters
        panel = adapters.lookup((providedBy(context),), IPanel, name=name)
        return Structure(panel(context, request, *args, **kw))

    @reify
    def context_url(self):
        return resource_url(self.context, self.request)

    @reify
    def app_url(self):
        return self.request.application_url

    @reify
    def bottlecap_static(self):
        return static_url('bottlecap:static/', self.request)

    @reify
    def global_nav_menus(self):
        # TODO we will need a way in sample/application (the custom
        # app) to reach over and grab lm instance to override
        menu_items = [
            dict(title="Item 1", selected=None),
            dict(title="Item 2", selected="selected"),
            dict(title="Item 3", selected=None),
            dict(title="Item 4", selected=None),
            dict(title="Item 5", selected=None),
            ]
        return menu_items


    # --
    # Head data and microtemplates management
    # --

    @property
    def head_data(self):
        if getattr(self, '_head_data', None) is None:
            self._head_data = {
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


class Structure(unicode):
    # Wrapping a string in this class avoids having to prefix the value
    # with `structure` in TAL

    def __html__(self):
        return self


def add_bc_layout(config, layout):
    settings = config.registry.settings
    bc = settings['bc']
    if isinstance(layout, dict):
        bc['layouts'] = layout


def add_bc_layoutmanager_factory(config, factory):
    factory = config.maybe_dotted(factory)
    config.registry.registerUtility(factory, ILayoutManagerFactory)

