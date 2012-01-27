from bottlecap.panel import panel_config

@panel_config(name='popper.global_nav',
              renderer='bottlecap:layouts/popper/templates/global_nav' \
                       '.pt')
def global_nav(context, request):
    nav_menu = [
        dict(title="Intranet",
             url=request.application_url,
             selected=None),
        dict(title="Communities",
             url=request.resource_url(context, 'communities'),
             selected=None),
        dict(title="People",
             url=request.resource_url(context, 'peopleosf'),
             selected=None),
        dict(title="Calendar", url='#', selected='selected'),
        dict(title="Feed", url='#', selected=None)]
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
