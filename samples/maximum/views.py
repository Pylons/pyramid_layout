from pyramid.view import view_config

class MaximumViews(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(name="peopleosf",
                 renderer="templates/peopleosf.pt")
    def peopleosf_view(self):
        """ The equivalent of /people/ """
        return {
            "project": "People Reports for OSF",
            "section_style": "compact",
        }

    @view_config(name="peopleosfbaltimore",
                 renderer="templates/peopleosfbaltimore.pt")
    def peopleosfbaltimore_view(self):
        return {
            "project": "Some Project",
            "section_style": "compact",
            }

    @view_config(name="communities",
                 renderer="templates/communities.pt")
    def communities_view(self):
        return {
            "project": "Some Project",
            "section_style": "none",
            }

    @view_config(renderer="templates/communitiesblog.pt")
    @view_config(name="communitiesblog",
                 renderer="templates/communitiesblog.pt")
    def communitiesblog_view(self):
        return {"project": "Africa Community"}

    ####

    @view_config('test', renderer="templates/testpage_view.pt")
    def testpage_view(self):
        self.request.layout_manager.use_layout('alternative')
        return {"project": "Some Project"}

