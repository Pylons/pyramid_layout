from pyramid.view import view_config

class SampleViews(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(name="peopleosf",
                 renderer="templates/peopleosf.pt")
    def peopleosf_view(self):
        """ The equivalent of /people/ """

        self.request.layout_manager.layout.show_sidebar = False
        self.request.layout_manager.layout.section_style = "compact"
        return {
            "project": "People Reports for OSF",
        }

    @view_config(name="peopleosfbaltimore",
                 renderer="templates/peopleosfbaltimore.pt")
    def peopleosfbaltimore_view(self):

        self.request.layout_manager.layout.show_sidebar = False
        self.request.layout_manager.layout.section_style = "compact"

        return {
            "project": "Some Project",
            }

    @view_config(name="communities",
                 renderer="templates/communities.pt")
    def communities_view(self):
        self.request.layout_manager.layout.section_style = "none"
        return {
            "project": "Some Project",
            }

    @view_config(renderer="templates/communitiesblog.pt")
    @view_config(name="communitiesblog",
                 renderer="templates/communitiesblog.pt")
    def communitiesblog_view(self):
        return {
            "project": "Africa Community",
        }

    ####

    @view_config('test', renderer="templates/testpage_view.pt")
    def testpage_view(self):
        self.request.layout_manager.use_layout('alternative')
        return {
            "project": "Some Project",
            "show_sidebar": True,
        }

