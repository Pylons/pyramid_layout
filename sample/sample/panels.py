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
        dict(id="communities",
             title="Communities",
             url=request.resource_url(context, 'communities'),
             selected=is_selected('communities')
             ),
        dict(id="people",
             title="People",
             url=request.resource_url(context, 'peopleosf'),
             selected=is_selected('peopleosf')
             ),
        dict(id="calendar",
             title="Calendar",
             url='#',
             selected=is_selected('calendar')
             ),
        dict(id="chatter",
             title="Chatter",
             url="#",
             selected=is_selected('chatter'),
             count="6"),
        dict(id="radar",
             title="Radar",
             url="#",
             selected=is_selected('radar'),
             count="7")]
    overflow = [
        dict(id="tagcloud",
             title="Tags",
             url='#',
             selected=is_selected('tagcloud'))]
    return {'nav_menu': nav_menu, 'overflow_menu': overflow}


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
