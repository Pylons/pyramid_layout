from pyramid.encode import urlencode

from bottlecap.panel import panel_config


@panel_config(name='popper.global_logo',
              renderer='templates/global_logo.pt')
def global_logo(context, request):
    return {'logo_href': request.application_url,
            'logo_title': 'Popper'}


@panel_config(name='popper.global_nav',
        renderer='templates/global_nav.pt')
def global_nav(context, request):
    nav_menu = [
        dict(title="Item 1", url='#', selected=None),
        dict(title="Item 2", url='#', selected="selected"),
        dict(title="Item 3", url='#', selected=None),
        dict(title="Item 4", url='#', selected=None),
        dict(title="Item 5", url='#', selected=None)]
    return {'nav_menu': nav_menu}


@panel_config(name='popper.personal_tools',
              renderer='templates/personal_tools.pt')
def personal_tools(context, request):
    return dict(profile_name="John Doe")


@panel_config(name='popper.context_tools',
              renderer='templates/context_tools.pt')
def context_tools(context, request, tools=None):
    """The context tools are a list of dicts with the keys:
       title, url and selected (None or 'selected').
       There's an additional optional key, dropdown, that
       can contain a list with more dicts in the same format
       to allow for one level of submenus."""
    return {'tools': tools}

@panel_config(name='popper.search', renderer='templates/search.pt')
def generic_panel(context, request):
    return {}


@panel_config(name='popper.actions_menu', renderer='templates/actions_menu.pt')
def action_menu(context, request):
    return {'actions': [
        {'title': 'Add', 'subactions': [
            {'title': 'Page', 'url': '#'},
            {'title': 'Folder', 'url': '#'},
            {'title': 'File', 'url': '#'},
            {'title': 'Blog Entry', 'url': '#'}]},
        {'title': 'Edit', 'url': '#'},
        {'title': 'Delete', 'url': '#', 'confirm': 'Are you sure?'}
    ]}

@panel_config(name='popper.tagbox', renderer='templates/tagbox.pt')
def tagbox(context, request):
    return {}

@panel_config(name='popper.site_announcement',
              renderer='templates/site_announcement.pt')
def site_announcement(context, request):
    if "show_announcement" not in request.params:
        # We only want to show the site announcement in the sample
        # app if we ask for it. We'll make a link on the sample page
        # to make this obvious
        return {}
    announcement = """
    Praesent commodo cursus magna, vel scelerisque nisl
        consectetur et. Sed posuere consectetur est at lobortis.
        Aenean eu leo quam. Pellentesque ornare sem lacinia quam
        venenatis vestibulum."""
    return dict(
        ann_headline="The dismissible site announcement",
        ann_body=announcement,
        ann_href="/",
    )

@panel_config(name='popper.grid_header', renderer='templates/grid_header.pt')
def grid_header(context, request, letters=None, filters=None, formats=None,
                actions=None):
    return {
        'letters': letters,
        'filters': filters,
        'formats': formats,
        'actions': actions}


@panel_config(name='popper.grid_footer', renderer='templates/grid_footer.pt')
def grid_footer(context, request, batch):
    # Pagination
    batch_size = batch['batch_size']
    n_pages = (batch['total'] - 1) / batch_size + 1
    if n_pages <= 1:
        batch['pagination'] = False
        return batch

    url = request.path_url
    def page_url(page):
        params = request.GET.copy()
        params['batch_start'] = str(page * batch_size)
        return '%s?%s' % (url, urlencode(params))

    batch['pagination'] = True
    current = batch['batch_start'] / batch['batch_size']
    if current > 0:
        batch['prev_url'] = page_url(current - 1)
    else:
        batch['prev_url'] = None
    if current + 1 < n_pages:
        batch['next_url'] = page_url(current + 1)
    else:
        batch['next_url'] = None
    pages = []
    for i in xrange(n_pages):
        ellipsis = i != 0 and i != n_pages - 1 and abs(current - i) > 3
        if ellipsis:
            if pages[-1]['name'] != 'ellipsis':
                pages.append({
                    'name': 'ellipsis',
                    'title': '...',
                    'url': None,
                    'selected': False})
        else:
            title = '%d' % (i + 1)
            pages.append({
                'name': title,
                'title': title,
                'url': page_url(i),
                'selected': i == current})

    batch['pages'] = pages
    return batch


@panel_config(name='popper.column_one', renderer='templates/column_one.pt')
def column_one(context, request):
    layout_manager = request.layout_manager
    layout = layout_manager.layout
    render = layout_manager.render_panel
    if layout.portlets:
        return '\n'.join(
            [render(name, *args, **kw)
             for name, args, kw in layout.portlets])
    return ''


@panel_config(name='popper.footer', renderer='templates/footer_panel.pt')
def footer(context, request):
    return {}


@panel_config(name='popper.extra_css')
def extra_css(context, request):
    layout = request.layout_manager.layout
    static_url = request.static_url
    css = []
    for spec in layout.extra_css:
        # We allow spec to be an absolute url, in which case
        # we "just use it".
        if not (spec.startswith('http://') or spec.startswith('https://')):
            spec = static_url(spec)
        css.append('\t\t<link rel="stylesheet" href="%s" />' % spec)
    return '\n'.join(css)


@panel_config(name='popper.extra_js')
def extra_js(context, request):
    layout = request.layout_manager.layout
    static_url = request.static_url
    js = []
    for spec in layout.extra_js:
        # We allow spec to be an absolute url, in which case
        # we "just use it".
        if not (spec.startswith('http://') or spec.startswith('https://')):
            spec = static_url(spec)
        # XXX We make it all defer. Revise and provide a parameter,
        # XXX if it makes sense!
        defer = True
        js.append('\t\t<script src="%s" %s></script>' % (spec, 'defer' if defer else ''))
    return '\n'.join(js)



# --
# Head resources.
# --
# You _probably_ want to inject your code into the
# non-head panels above, instead of here.
# You want to add here only 3rdparty
# libs that initiate more loading, so they should happen
# as early as possible. (Like, google stuff.)
# --

@panel_config(name='popper.extra_css_head')
def extra_css_head(context, request):
    layout = request.layout_manager.layout
    static_url = request.static_url
    css = []
    for spec in layout.extra_css_head:
        # We allow spec to be an absolute url, in which case
        # we "just use it".
        if not (spec.startswith('http://') or spec.startswith('https://')):
            spec = static_url(spec)
        css.append('\t\t<link rel="stylesheet" href="%s" />' % spec)
    return '\n'.join(css)


@panel_config(name='popper.extra_js_head')
def extra_js_head(context, request):
    layout = request.layout_manager.layout
    static_url = request.static_url
    js = []
    for spec in layout.extra_js_head:
        # We allow spec to be an absolute url, in which case
        # we "just use it".
        if not (spec.startswith('http://') or spec.startswith('https://')):
            spec = static_url(spec)
        # XXX We make it all non-defer. Revise and provide a parameter,
        # XXX if it makes sense!
        defer = False
        js.append('\t\t<script src="%s" %s></script>' % (spec, 'defer' if defer else ''))
    return '\n'.join(js)


# Can be use to insert arbitrary construct into the head slot.
# Similar result as inserting from the view into the head_slot of the template,
# but it is easier accessible from the layout 
# if global script code has to be inserted here.
@panel_config(name='popper.extra_slot_head')
def extra_head(context, request):
    return ''
 
