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
        self.request.layout_manager.layout.section_style = "compact"
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


    @view_config(name='livesearch.json', renderer="json", xhr=True)
    def livesearch_ajax_view(self):
        # Example result set, for demonstrating the widget without
        # a real server database.
        headshot_url = self.request.static_url('bottlecap.layouts.popper:static/popper-plugins/popper-livesearch/images/headshot.jpg')
        icon_url = self.request.static_url('bottlecap.layouts.popper:static/popper-plugins/popper-livesearch/images/xls_small.gif')

        result = [{"category": "profile", "extension": "1984", "title":
            "Janos Kovacs", "url":
            "https://karl.soros.org/profiles/nborland/", "email":
            "mail@example.com", "department": "Information Systems, Knowledge Management Initiative", "type": "profile", "thumbnail":
            headshot_url},
            {"category": "profile", "extension": "1382", "title": "Janos Kovacs",
            "url": "https://karl.soros.org/profiles/tmoroz/", "email":
            "mail@example.com", "department": "Information Systems, Knowledge Management Initiative", "type": "profile", "thumbnail":
            headshot_url},
            {"category": "profile", "extension": "1643", "title": "Janos Kovacs", "url": "https://karl.soros.org/profiles/rmarianski/",
            "email": "mail@example.com", "department": "Information Systems, Knowledge Management Initiative", "type": "profile", "thumbnail":
            headshot_url},
            {"category": "profile", "extension": "1937", "title": "Janos Kovacs",
            "url": "https://karl.soros.org/profiles/ajoseph/", "email":
            "mail@example.com", "department": "Information Systems", "type":
            "profile", "thumbnail":
            headshot_url},
            {"category": "profile", "extension": "4000", "title": "Janos Kovacs", "url": "https://karl.soros.org/profiles/fuzesisz/", "email":
            "mail@example.com", "department": "Information Systems", "type":
            "profile", "thumbnail":
            headshot_url},
            {"category": "page", "modified_by": "emcgonagill", "title": "KARL User Manual", "url":
            "https://karl.soros.org/communities/about-karl/wiki/karl-user-manual/",
            "type": "page", "modified": "2011-06-17T11:03:17.597440", "community":
            "About KARL, KARL Online Manual"}, {"category": "page", "modified_by":
            "nborland", "title": "Contact", "url":
            "https://karl.soros.org/contact/", "type": "page", "modified":
            "2009-07-17T13:48:53.210301", "community": None}, {"category": "page",
            "modified_by": "nborland", "title": "Karl Administration Community Wiki Page", "url":
            "https://karl.soros.org/communities/karl-administration/wiki/front_page/",
            "type": "page", "modified": "2010-10-15T14:48:03.932662", "community":
            "Karl Administration"}, {"category": "page", "modified_by":
            "emcgonagill", "title": "5. Fostering KARL as open source", "url":
            "https://karl.soros.org/communities/karl-team-hub/wiki/5.-fostering-karl-as-open-source/",
            "type": "page", "modified": "2010-10-14T15:42:29.676338", "community":
            "KARL Team Hub"}, {"category": "page", "modified_by": "ree", "title":
            "Paul Private Community Wiki Page", "url":
            "https://karl.soros.org/communities/paul-private/wiki/front_page/",
            "type": "page", "modified": "2010-08-30T12:08:04.785350", "community":
            "Paul Private"}, {"category": "blogentry", "modified_by": None,
            "title": "KARL can be really slow", "url":
            "https://karl.soros.org/communities/karl-feedback-community/blog/karl-can-be-really-slow/",
            "type": "post", "modified": "2008-02-14T14:02:11", "community": "KARL Feedback Community"}, {"category": "blogentry", "modified_by": None,
            "title": "out of office replies / sending emails", "url":
            "https://karl.soros.org/communities/karl-feedback-community/blog/out-of-office-replies-sending-emails/",
            "type": "post", "modified": "2008-08-06T08:29:53", "community": "KARL Feedback Community"}, {"category": "blogentry", "modified_by": None,
            "title": "tag listing problem", "url":
            "https://karl.soros.org/communities/karl-feedback-community/blog/tag-listing-problem/",
            "type": "post", "modified": "2009-02-09T04:18:10", "community": "KARL Feedback Community"}, {"category": "blogentry", "modified_by": None,
            "title": "London's talking", "url":
            "https://karl.soros.org/communities/karl-feedback-community/blog/londons-talking/",
            "type": "post", "modified": "2007-06-04T16:23:39", "community": "KARL Feedback Community"}, {"category": "blogentry", "modified_by": None,
            "title": "inadvertent comments", "url":
            "https://karl.soros.org/communities/karl-feedback-community/blog/inadvertent-comments/",
            "type": "post", "modified": "2007-06-01T12:39:53", "community": "KARL Feedback Community"}, {"category": "file", "modified_by": None,
            "title": "KARL instructions", "url":
            "https://karl.soros.org/communities/insaan-group/files/karl-instructions-7.30.07.doc/",
            "modified": "2007-08-21T16:06:49", "community": "Insaan Group", "type":
            "file", "icon":
            icon_url},
            {"category": "file", "modified_by": "nborland", "title": "KARL Doc",
            "url":
            "https://karl.soros.org/communities/its-a-test/files/nyc/accessing-the-karl-global-staff-administrator-9.17.doc/",
            "modified": "2010-05-18T10:19:10.714191", "community": "It's a Test",
            "type": "file", "icon":
            icon_url},
            {"category": "file", "modified_by": None, "title": "KARL Terms of Service", "url":
            "https://karl.soros.org/communities/karl-legal-privacy-issues/files/clean-6-1-2007-generic_tos_for_osi.doc/",
            "modified": "2007-06-07T15:22:03", "community": "KARL Legal / Privacy Issues", "type": "file", "icon":
            icon_url},
            {"category": "file", "modified_by": "tmoroz", "title": "Another Files Goes Here", "url":
            "https://karl.soros.org/communities/training/files/information-management-worksho1.doc/",
            "modified": "2010-04-05T04:52:52.260346", "community": "Training",
            "type": "file", "icon":
            icon_url},
            {"category": "file", "modified_by": "nborland", "title": "Thursday File", "url":
            "https://karl.soros.org/communities/training/files/karl-staff-info-sheet.xls/",
            "modified": "2011-03-03T11:36:41.410971", "community": "Training",
            "type": "file", "icon":
            icon_url},
            {"category": "calendarevent", "end": "2007-05-16T10:30:00", "title":
            "KARL-beta demo & discussion", "url":
            "https://karl.soros.org/communities/km-working-group/calendar/karl-beta-demo-discussion/",
            "community": "KM Working Group", "start": "2007-05-16T09:30:00",
            "location": "NY, 4E   Budapest, room 401", "type": "calendarevent"},
            {"category": "calendarevent", "end": "2011-06-30T09:00:00", "title":
            "Bootcamp meetup", "url":
            "https://karl.soros.org/communities/training/calendar/bootcamp-meetup/",
            "community": "Training", "start": "2011-06-30T08:00:00", "location":
            "", "type": "calendarevent"}, {"category": "calendarevent", "end":
            "2010-04-07T11:00:00", "title": "KARL Support Staff Weekly Meeting",
            "url":
            "https://karl.soros.org/communities/karl-support/calendar/karl-support-staff-weekly-meeting/",
            "community": "KARL Support", "start": "2010-04-07T10:00:00",
            "location": "Skype", "type": "calendarevent"}, {"category":
            "calendarevent", "end": "2008-12-04T13:00:00", "title": "Brown-Bag Lunch: KARL Update", "url":
            "https://karl.soros.org/offices/budapest/office-events/brown-bag-lunch-karl-update/",
            "community": "Budapest", "start": "2008-12-04T12:00:00", "location":
            "", "type": "calendarevent"}, {"category": "calendarevent", "end":
            "2010-01-27T13:00:00", "title": "KARL Calendar Training", "url":
            "https://karl.soros.org/communities/karl-feedback-community/calendar/karl-calendar-training-1/",
            "community": "KARL Feedback Community", "start": "2010-01-27T12:00:00",
            "location": "New York 4E", "type": "calendarevent"}, {"url":
            "https://karl.soros.org/communities/karl-consortium/", "category":
            "community", "num_members": 33, "type": "community", "title": "KARL Consortium"}, {"url":
            "https://karl.soros.org/communities/a-time-for-testing-again/",
            "category": "community", "num_members": 4, "type": "community",
            "title": "A Time for Testing: Again"}, {"url":
            "https://karl.soros.org/communities/paul-test-tries/", "category":
            "community", "num_members": 2, "type": "community", "title": "Paul Test Community"}, {"url":
            "https://karl.soros.org/communities/paul-private/", "category":
            "community", "num_members": 1, "type": "community", "title": "Paul Private"}, {"url": "https://karl.soros.org/communities/karl-support/",
            "category": "community", "num_members": 6, "type": "community",
            "title": "KARL Support"}]
        return result

