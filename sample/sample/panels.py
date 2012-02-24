from bottlecap.panel import panel_config

@panel_config(name='popper.global_nav',
              renderer='bottlecap:layouts/popper/templates/global_nav' \
                       '.pt')
def global_nav(context, request):
    def is_selected(item):
        if request.path == '/' and not item:
            return 'selected'
        elif request.path.startswith('/{0}'.format(item)) and item:
            return 'selected'
        return None
    nav_menu = [
        dict(title="Communities",
             url=request.resource_url(context, 'communities'),
             selected=is_selected('communities')
             ),
        dict(title="People",
             url=request.resource_url(context, 'peopleosf'),
             selected=is_selected('peopleosf')
             ),
        dict(title="Calendar",
             url='#',
             selected=is_selected('calendar')
             )]
    return {'nav_menu': nav_menu}


@panel_config(name='sample.content_portlet',
              renderer='templates/content_portlet.pt')
@panel_config(name='sample.section_portlet',
              renderer='templates/section_portlet.pt')
def generic_portlet(context, request):
    return {}

@panel_config(
    name='sample.community_portlet',
    renderer='templates/community_portlet.pt'
    )
def community_portlet(context, request):
  return {}
