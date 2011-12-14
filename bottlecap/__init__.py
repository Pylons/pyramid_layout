from pyramid.events import BeforeRender

from bottlecap.layout import (
        ILayoutManagerFactory,
        LayoutManager,
        add_bc_layout,
        add_bc_layoutmanager_factory
        )


def add_renderer_globals(event):
    # Note that, since we have so many renderings going on now (due to
    # layout components), this gets called 8 times or so
    request = event['request']
    context = request.context
    settings = request.registry.settings
    bc = settings['bc']
    _lm = request.registry.queryUtility(ILayoutManagerFactory)
    if not _lm:
        _lm = LayoutManager
    lm = _lm(context, request)
    if 'layouts' in bc:
        lm._add_layout(bc['layouts'])
    event['lm'] = lm

    # If being called on a layout component, the econtext of the calling
    # template will be stashed away on the request.  This should be used
    # to update the globals.  It shouldn't clobber anything already added.
    econtext = getattr(request, '_parent_econtext', None)
    if econtext:
        for k, v in econtext.items():
            if k not in event:
                event[k] = v


def includeme(config):
    config.registry.settings['bc'] = {}
    config.scan('bottlecap.views')
    config.add_directive('add_bc_layout', add_bc_layout)
    config.add_directive('add_bc_layoutmanager_factory',
            add_bc_layoutmanager_factory)
    config.add_subscriber(add_renderer_globals, BeforeRender)
    config.add_static_view('bc-static', 'bottlecap:static/',
            cache_max_age=86400)
