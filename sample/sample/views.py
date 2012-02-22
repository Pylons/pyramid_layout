
import datetime
import random

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
        letters = [{'name': chr(ch),
                    'href': '#' if ch in (67, 69, 75) else None,
                    'is_current': True if ch == 80 else False}
                   for ch in xrange(ord('A'), ord('Z') + 1)]
        actions = [
            {'name': 'print', 'title': 'Print',
             'description': 'Print this report',
             'url': self.request.resource_url(self.context, 'print.html')},
            {'name': 'csv', 'title': 'Export as CSV',
             'description': 'Export this report as CSV',
             'url': self.request.resource_url(self.context, 'csv')}]

        formats = [
            {'name': 'tabular', 'title': 'Tabular view', 'selected': True,
             'description': 'View as a table',
             'url': self.request.resource_url(self.context)},
            {'name': 'picture', 'title': 'Picture view', 'selected': False,
             'description': "View as portraits",
             'url': self.request.resource_url(self.context, query={
                 'format': 'picture'})}]

        total = 188
        size = 10
        begin = int(self.request.GET.get('batch_start', 0))
        end = min(begin + size, total)
        batch = {
            'batch_start': begin,
            'batch_end': end,
            'total': total,
            'batch_size': size,
        }

        return {
            'letters': letters,
            'actions': actions,
            'formats': formats,
            'batch': batch}

    @view_config(name="communities",
                 renderer="templates/communities.pt")
    def communities_view(self):
        layout = self.request.layout_manager.layout
        #layout.show_sidebar = True
        layout.section_style = "none"
        layout.add_portlet('sample.community_portlet')

        filters = [
                {'name': 'attractive', 'title': 'Attractive',
                 'selected': False,
                 'description': 'Show only attractive people', 'url': '#'},
                {'name': 'all', 'title': 'All', 'selected': True,
                 'description': 'Show all people', 'url': '#'}]

        letters = [{'name': chr(ch),
                    'href': '#' if ch in (67, 69, 75) else None,
                    'is_current': True if ch == 80 else False}
        for ch in xrange(ord('A'), ord('Z') + 1)]

        total = 188
        size = 10
        begin = int(self.request.GET.get('batch_start', 0))
        end = min(begin + size, total)
        batch = {
            'batch_start': begin,
            'batch_end': end,
            'total': total,
            'batch_size': size,
            }

        return {
            "project": "Some Project",
            'letters': letters,
            'filters': filters,
            'batch': batch
        }

    @view_config(renderer="templates/index.pt")
    def index_view(self):
        layout = self.request.layout_manager.layout
        layout.add_portlet('sample.content_portlet')
        layout.add_portlet('sample.community_portlet')

        return {}

    @view_config(name="communitiesblog",
                 renderer="templates/communitiesblog.pt")
    def communitiesblog_view(self):
        layout = self.request.layout_manager.layout
        layout.add_portlet('popper.tagbox')
        layout.add_portlet('sample.content_portlet')
        layout.add_portlet('sample.section_portlet')
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

        result = [{"category": "profile", "extension": "1234", "title":
            "Janos Kovacs", "url":
            "https://foo.bar/", "email":
            "mail@example.com", "department": "Department 1", "type": "profile", "thumbnail":
            headshot_url},
            {"category": "profile", "extension": "1234", "title": "Janos Kovacs",
            "url": "https://foo.bar/", "email":
            "mail@example.com", "department": "Department 1", "type": "profile", "thumbnail":
            headshot_url},
            {"category": "profile", "extension": "1234", "title": "Janos Kovacs", "url": "http://foo.bar/",
            "email": "mail@example.com", "department": "Department 1", "type": "profile", "thumbnail":
            headshot_url},
            {"category": "profile", "extension": "1234", "title": "Janos Kovacs",
            "url": "https://foo.bar/", "email":
            "mail@example.com", "department": "Department 2", "type":
            "profile", "thumbnail":
            headshot_url},
            {"category": "profile", "extension": "1234", "title": "Janos Kovacs", "url": "https://foo.bar", "email":
            "mail@example.com", "department": "Department 2", "type":
            "profile", "thumbnail":
            headshot_url},
            {"category": "page", "modified_by": "user1", "title": "Title 1", "url":
            "https://foo.bar/",
            "type": "page", "modified": "2011-06-17T11:03:17.597440", "community":
            "About KARL, KARL Online Manual"}, {"category": "page", "modified_by":
            "user2", "title": "Contact", "url":
            "https://foo.bar/", "type": "page", "modified":
            "2009-07-17T13:48:53.210301", "community": None}, {"category": "page",
            "modified_by": "user1", "title": "Title 1", "url":
            "https://foo..bar/",
            "type": "page", "modified": "2010-10-15T14:48:03.932662", "community":
            "community 1"}, {"category": "page", "modified_by":
            "user1", "title": "Title 2", "url":
            "https://foo.bar",
            "type": "page", "modified": "2010-10-14T15:42:29.676338", "community":
            "Community 2"}, {"category": "page", "modified_by": "ree", "title":
            "Ree's Private Community Wiki Page", "url":
            "https://foo.bar",
            "type": "page", "modified": "2010-08-30T12:08:04.785350", "community":
            "Community 3"}, {"category": "blogentry", "modified_by": None,
            "title": "Title 3", "url":
            "https://foo.bar/",
            "type": "post", "modified": "2008-02-14T14:02:11", "community": "Community 1"}, {"category": "blogentry", "modified_by": None,
            "title": "Title 4", "url":
            "https://foo.bar/",
            "type": "post", "modified": "2008-08-06T08:29:53", "community": "Community 1"}, {"category": "blogentry", "modified_by": None,
            "title": "Title 5", "url":
            "https://foo.bar/",
            "type": "post", "modified": "2009-02-09T04:18:10", "community": "Community 2"}, {"category": "blogentry", "modified_by": None,
            "title": "Title 6", "url":
            "https://foo.bar/",
            "type": "post", "modified": "2007-06-04T16:23:39", "community": "Community 2"}, {"category": "blogentry", "modified_by": None,
            "title": "Title 7", "url":
            "https://foo.bar/",
            "type": "post", "modified": "2007-06-01T12:39:53", "community": "Community 2"}, {"category": "file", "modified_by": None,
            "title": "Title 8", "url":
            "https://foo.bar/",
            "modified": "2007-08-21T16:06:49", "community": "Community 3", "type":
            "file", "icon":
            icon_url},
            {"category": "file", "modified_by": "user3", "title": "Title 9",
            "url":
            "https:/foo.bar/",
            "modified": "2010-05-18T10:19:10.714191", "community": "Community 4",
            "type": "file", "icon":
            icon_url},
            {"category": "file", "modified_by": None, "title": "Community 5", "url":
            "https://foo.bar/",
            "modified": "2007-06-07T15:22:03", "community": "Community 1", "type": "file", "icon":
            icon_url},
            {"category": "file", "modified_by": "user7", "title": "Title 10", "url":
            "https://foo.bar",
            "modified": "2010-04-05T04:52:52.260346", "community": "Community 4",
            "type": "file", "icon":
            icon_url},
            {"category": "file", "modified_by": "user5", "title": "Title 11", "url":
            "https://foo.bar",
            "modified": "2011-03-03T11:36:41.410971", "community": "Community 5",
            "type": "file", "icon":
            icon_url},
            {"category": "calendarevent", "end": "2007-05-16T10:30:00", "title":
            "Title 12", "url":
            "http://foo.bar",
            "community": "Community 2", "start": "2007-05-16T09:30:00",
            "location": "Room East", "type": "calendarevent"},
            {"category": "calendarevent", "end": "2011-06-30T09:00:00", "title":
            "Title 13", "url":
            "https://foo.bar/",
            "community": "Community 3", "start": "2011-06-30T08:00:00", "location":
            "", "type": "calendarevent"}, {"category": "calendarevent", "end":
            "2010-04-07T11:00:00", "title": "Title 14",
            "url":
            "https://foo.bar",
            "community": "Community 4", "start": "2010-04-07T10:00:00",
            "location": "Room East", "type": "calendarevent"}, {"category":
            "calendarevent", "end": "2008-12-04T13:00:00", "title": "Title 15", "url":
            "https://foo.bar/",
            "community": "Community 4", "start": "2008-12-04T12:00:00", "location":
            "", "type": "calendarevent"}, {"category": "calendarevent", "end":
            "2010-01-27T13:00:00", "title": "Title 16", "url":
            "https://foo.bar",
            "community": "Community 5", "start": "2010-01-27T12:00:00",
            "location": "Room West", "type": "calendarevent"}, {"url":
            "https://foo.bar", "category":
            "community", "num_members": 33, "type": "community", "title": "Title 17"}, {"url":
            "https://foo.bar/",
            "category": "community", "num_members": 4, "type": "community",
            "title": "Title 18"}, {"url":
            "https://foo.bar/", "category":
            "community", "num_members": 2, "type": "community", "title": "Title 18"}, {"url":
            "https://foo.bar", "category":
            "community", "num_members": 1, "type": "community", "title": "Title 19"}, {"url": "http://foo.bar/",
            "category": "community", "num_members": 6, "type": "community",
            "title": "Title 20"}]
        return result


    @view_config(name='notifier.json', renderer="json", xhr=True)
    def notifier_ajax_view(self):
        # Example result set, for demonstrating without
        # a real server database.
        
        # XXX This method should dispatch a call to each catalog
        # search that needs to be notified.
        # It only needs to provide the recent counters in the resulting payload.

        # The request contains parameters for each notification source, keyed
        # by their name. The value is a date which contains the end of the last
        # succesful query.

        updates = {}
        for name, value in self.request.params.iteritems():
            # value is in isodate format, let's convert it to a real datetime.
            d = datetime.datetime.strptime(value.split('.')[0], '%Y-%m-%dT%H:%M:%S')
            updates[name] = d
        # ... for example update['chatter'] now contains the start-date that the
        # chatter query will need.
        
        now = datetime.datetime.now()
        now_iso = now.isoformat()
        # Only those pushdowns are notified, who are in the dictionary.
        notifications = {}
        for name in ['chatter']:
            # XXX do a real query from here, using updates[name] for start date.
            notifications[name] = dict(
                cnt = random.choice([0, random.randrange(1, 5)]),
                ts = now_iso, 
                )

        return notifications


    @view_config(name='chatter.json', renderer="json", xhr=True)
    def chatter_ajax_view(self):
        # Example result set, for demonstrating the widget without
        # a real server database.
        results = {}
        if self.request.params.get('needsTemplate', 'false') in ('true', 'True'):
            # We need the template. So, let's fetch it.
            layout = self.request.layout_manager.layout
            results['microtemplate'] = layout.microtemplates['chatter']
        # Fetch the data
        results['data'] = {
            'streams': [{
                'class': 'your-stream',
                'title': 'Direct messages',
                'has_more_news': False,
                'items': [{
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '3 min ago',
                        'new': True,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'John Doe',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volu',
                        'info': '5 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }],
                }, {
                'class': 'recent-friend',
                'title': 'Friends activity',
                'has_more_news': True,
                'items': [{
                        'author': 'John Doe',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volu',
                        'info': '3 min ago',
                        'new': True,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volu',
                        'info': '4 min ago',
                        'new': True,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': True,
                    }, {
                        'author': 'John Doe',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volu',
                        'info': '5 min ago',
                        'new': True,
                    }],
                }],
            }
        return results


    @view_config(name='radar.json', renderer="json", xhr=True)
    def radar_ajax_view(self):
        # Example result set, for demonstrating the widget without
        # a real server database.
        results = {}
        if self.request.params.get('needsTemplate', 'false') in ('true', 'True'):
            # We need the template. So, let's fetch it.
            layout = self.request.layout_manager.layout
            results['template'] = layout.templates['radar']

        results['data'] = {
            'streams': [{
                'class': 'stream1',
                'title': 'What do we list here?',
                'items': [{
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }],
                }, {
                'class': 'stream2',
                'title': 'Private messages???',
                'items': [{
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }],
                }, {
                'class': 'stream3',
                'title': 'Private messages again???',
                'items': [{
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }, {
                        'author': 'Tester Testerson',
                        'author_profile_url': '#author_profile',
                        'message_url': '#message',
                        'image_url': 'http://twimg0-a.akamaihd.net/profile_images/413225762/python_normal.png',
                        'text': 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at ve.',
                        'info': '4 min ago',
                        'new': False,
                    }],
                }],
            }
        return results

