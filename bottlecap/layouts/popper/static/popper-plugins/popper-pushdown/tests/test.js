/*jslint undef: true, newcap: true, nomen: false, white: true, regexp: true */
/*jslint plusplus: false, bitwise: true, maxerr: 50, maxlen: 80, indent: 4 */
/*jslint sub: true */
/*globals window navigator document console setTimeout jQuery module test $ */
/*globals module test start stop expect equal same ok raises */


var log = function () {
    if (window.console && console.log) {
        // log for FireBug or WebKit console
        console.log(Array.prototype.slice.call(arguments));
    }
};

 
module('popper-pushdowntab', {

    setup: function () {
        var self = this;
        $('#main').append(
            '<div id="the-top-bar">' +
                '<a id="the-link">' +
                    'Pushdown <span class="the-counter">11</span>' +
                '</a>' +
            '</div>'
        );
        // Mock stub for Mustache, which we assume to be tested by itself.
        this.Mustache_orig = window.Mustache;
        window.Mustache = {
            to_html: function (template, data) {
                return template;
            }
        };

        // XXX XXX
        window.head_data = {
            microtemplates: {mypushdown: 'THIS IS A PUSHDOWN'},
            panel_data: {mypushdown: {}}
        };

    },

    teardown: function () {
        window.Mustache = this.Mustache_orig;
        this.Mustache_orig = null;
        $('#main').empty();
    }

});


test("Create / destroy", function () {

    $('#the-link').pushdowntab({
        name: 'mypushdown',
        selectTopBar: '#the-top-bar',
        findCounterLabel: '.the-counter'
    });

    $('#the-link').pushdowntab('destroy');

    ok(true);
});


test("open it", function () {
    stop();
    expect(3);

    $('#the-link').pushdowntab({
        name: 'mypushdown',
        selectTopBar: '#the-top-bar',
        findCounterLabel: '.the-counter'
    });
    ok($('#popper-pushdown-mypushdown').length > 0);
    equal($('#popper-pushdown-mypushdown').is(':visible'), false);
    
    $('#the-link').simulate('click');

    // wait for animation finished
    setTimeout(function () {
        equal($('#popper-pushdown-mypushdown').is(':visible'), true);
        $('#the-link').pushdowntab('destroy');
        start();
    }, 400);

});


test("close it", function () {
    stop();
    expect(4);

    $('#the-link').pushdowntab({
        name: 'mypushdown',
        selectTopBar: '#the-top-bar',
        findCounterLabel: '.the-counter'
    });
    ok($('#popper-pushdown-mypushdown').length > 0);
    equal($('#popper-pushdown-mypushdown').is(':visible'), false);
    
    // click to open it
    $('#the-link').simulate('click');

    // wait for animation finished
    setTimeout(function () {
        equal($('#popper-pushdown-mypushdown').is(':visible'), true);
        
        // click again to close it
        $('#the-link').simulate('click');

        setTimeout(function () {
            equal($('#popper-pushdown-mypushdown').is(':visible'), false);
            $('#the-link').pushdowntab('destroy');
            start();
        }, 200);
    }, 400);

});


test("trigger events beforeShow, show, beforeHide, hide", function () {
    stop();
    expect(9);

    var events = [];
    function markEvent(evt) {
        events.push(evt.type);
    }

    $('#the-link').pushdowntab({
        name: 'mypushdown',
        selectTopBar: '#the-top-bar',
        findCounterLabel: '.the-counter',
        beforeShow: markEvent,
        show: markEvent,
        beforeHide: markEvent,
        hide: markEvent
    });
    ok($('#popper-pushdown-mypushdown').length > 0);
    equal($('#popper-pushdown-mypushdown').is(':visible'), false);
    same(events, []);

    // click to open it
    $('#the-link').simulate('click');
    same(events, ['pushdowntabbeforeshow']);

    // wait for animation finished
    setTimeout(function () {
        equal($('#popper-pushdown-mypushdown').is(':visible'), true);
        same(events, 
            ['pushdowntabbeforeshow', 'pushdowntabshow']);

        // click again to close it
        $('#the-link').simulate('click');
        same(events,
            ['pushdowntabbeforeshow', 'pushdowntabshow',
            'pushdowntabbeforehide']);

        setTimeout(function () {
            equal($('#popper-pushdown-mypushdown').is(':visible'), false);
            same(events,
                ['pushdowntabbeforeshow', 'pushdowntabshow',
                'pushdowntabbeforehide', 'pushdowntabhide']);
            $('#the-link').pushdowntab('destroy');
            start();
        }, 200);
    }, 400);

});


test("getCounter method", function () {
    $('#the-link').pushdowntab({
        name: 'mypushdown',
        selectTopBar: '#the-top-bar',
        findCounterLabel: '.the-counter'
    });

    equal($('#the-link').pushdowntab('getCounter'), 11);

    $('#the-link .the-counter').text('');
    equal($('#the-link').pushdowntab('getCounter'), 0);

    $('#the-link .the-counter').text('NOTNUMBER');
    equal($('#the-link').pushdowntab('getCounter'), 0);

    $('#the-link .the-counter').text('12.12');
    equal($('#the-link').pushdowntab('getCounter'), 12);

    $('#the-link .the-counter').text('-12');
    equal($('#the-link').pushdowntab('getCounter'), 0);
});


test("setCounter method", function () {
    $('#the-link').pushdowntab({
        name: 'mypushdown',
        selectTopBar: '#the-top-bar',
        findCounterLabel: '.the-counter'
    });

    // we are closed now
    ok($('#popper-pushdown-mypushdown').length > 0);
    equal($('#popper-pushdown-mypushdown').is(':visible'), false);

    $('#the-link').pushdowntab('setCounter', 3);
    equal($('#the-link .the-counter').text(), '3');
    equal($('#the-link .the-counter').is(':visible'), true);

    $('#the-link').pushdowntab('setCounter', 44);
    equal($('#the-link .the-counter').text(), '44');
    equal($('#the-link .the-counter').is(':visible'), true);

    $('#the-link').pushdowntab('setCounter', 0);
    equal($('#the-link .the-counter').text(), '0');
    equal($('#the-link .the-counter').is(':visible'), false,
            'if counter is zero, it is hidden');

    $('#the-link').pushdowntab('setCounter', 2);
    equal($('#the-link .the-counter').text(), '2');
    equal($('#the-link .the-counter').is(':visible'), true);

});


test("listens to notifierUpdate event when panel is closed", function () {
    $('#the-link').pushdowntab({
        name: 'mypushdown',
        selectTopBar: '#the-top-bar',
        findCounterLabel: '.the-counter'
    });

    // we are closed now
    ok($('#popper-pushdown-mypushdown').length > 0);
    equal($('#popper-pushdown-mypushdown').is(':visible'), false);

    // initially we are on 11
    equal($('#the-link').pushdowntab('getCounter'), 11);

    // notifier will trigger this events on document, so this
    // is the same what we test here.

    $(document).trigger('notifierUpdate', [{
        mypushdown: {cnt: 2, ts: '2012-02-13T20:40:24.771787'},
        // foo is, of course, ignored altogether.
        foo: {cnt: 99, ts: '2012-02-13T20:40:24.771787'}
    }]);
    equal($('#the-link').pushdowntab('getCounter'), 13);

    $(document).trigger('notifierUpdate', [{
        // different isodate format is also ok.
        mypushdown: {cnt: 3, ts: '2012-2-13T20:40:24'}, 
        foo: {cnt: 99, ts: '2012-02-13T20:40:24.771787'}
    }]);
    equal($('#the-link').pushdowntab('getCounter'), 16);

    $(document).trigger('notifierUpdate', [{
        // cnt = 0
        mypushdown: {cnt: 0, ts: '2012-02-13T20:40:24.771787'},
        foo: {cnt: 99, ts: '2012-02-13T20:40:24.771787'}
    }]);
    equal($('#the-link').pushdowntab('getCounter'), 16);

    $(document).trigger('notifierUpdate', [{
        // no section for this pushdown
        foo: {cnt: 99, ts: '2012-02-13T20:40:24.771787'}
    }]);
    equal($('#the-link').pushdowntab('getCounter'), 16);

});


test("listens to notifierUpdate event when panel open", function () {
    stop();
    expect(11);
    
    $('#the-link').pushdowntab({
        name: 'mypushdown',
        selectTopBar: '#the-top-bar',
        findCounterLabel: '.the-counter'
    });

    // we are closed now
    ok($('#popper-pushdown-mypushdown').length > 0);
    equal($('#popper-pushdown-mypushdown').is(':visible'), false);

    // initially we are on 11
    equal($('#the-link').pushdowntab('getCounter'), 11);

    // open it 
    $('#the-link').simulate('click');

    // wait for animation finished
    setTimeout(function () {
        equal($('#popper-pushdown-mypushdown').is(':visible'), true);

        // label is zero and hidden now, since we are opened
        equal($('#the-link').pushdowntab('getCounter'), 0);
        equal($('#the-link .the-counter').is(':visible'), false);

        // notifier will trigger this events on document, so this
        // is the same what we test here.

        $(document).trigger('notifierUpdate', [{
            mypushdown: {cnt: 22, ts: '2012-02-13T20:40:24.771787'},
            // foo is, of course, ignored altogether.
            foo: {cnt: 99, ts: '2012-02-13T20:40:24.771787'}
        }]);

        // however in open state, the counter will always remain intact
        equal($('#the-link').pushdowntab('getCounter'), 0);
        equal($('#the-link .the-counter').is(':visible'), false);
        
        // click again to close it
        $('#the-link').simulate('click');

        setTimeout(function () {
            equal($('#popper-pushdown-mypushdown').is(':visible'), false);

            $(document).trigger('notifierUpdate', [{
                mypushdown: {cnt: 33, ts: '2012-02-13T20:40:24.771787'},
                // foo is, of course, ignored altogether.
                foo: {cnt: 99, ts: '2012-02-13T20:40:24.771787'}
            }]);

            // counter re-appeared, but we only have the recent items
            // since the panel has been closed.
            equal($('#the-link').pushdowntab('getCounter'), 33);
            equal($('#the-link .the-counter').is(':visible'), true);

            $('#the-link').pushdowntab('destroy');
            start();
        }, 200);

    }, 400);
});



module('popper-pushdownpanel', {
    // Pushdownpanel is a slave of pushdowntab.
    setup: function () {
        var self = this;
        $('#main').append(
            '<div id="the-node">The Pushdown Text</div>'
        );
    },

    teardown: function () {
        $('#main').empty();
    }

});


test("Create / destroy", function () {

    $('#the-node').pushdownpanel({
    });

    $('#the-node').pushdownpanel('destroy');

    ok(true);
});


test("show", function () {
    stop();
    expect(2);

    $('#the-node').pushdownpanel({
    });

    equal($('#the-node').is(':visible'), false);
    
    $('#the-node').pushdownpanel('show');

    // wait for animation finished
    setTimeout(function () {
        equal($('#the-node').is(':visible'), true);
        $('#the-node').pushdownpanel('destroy');
        start();
    }, 400);

});


test("hide", function () {
    stop();
    expect(3);

    // create, and see that is is not visible
    $('#the-node').pushdownpanel({
    });
    equal($('#the-node').is(':visible'), false);
    
    // show it
    $('#the-node').pushdownpanel('show');

    // wait for animation finished
    setTimeout(function () {
        equal($('#the-node').is(':visible'), true);

        // hide it
        $('#the-node').pushdownpanel('hide');

        setTimeout(function () {
            equal($('#the-node').is(':visible'), false);
            $('#the-node').pushdownpanel('destroy');
            start();
        }, 200);
    }, 400);

});


test("show while showing", function () {
    stop();
    expect(2);

    // create, and see that is is not visible
    $('#the-node').pushdownpanel({
    });
    equal($('#the-node').is(':visible'), false);
    
    // show it
    $('#the-node').pushdownpanel('show');

    // show it again
    $('#the-node').pushdownpanel('show');

    // wait for animation finished
    setTimeout(function () {
        equal($('#the-node').is(':visible'), true);
        $('#the-node').pushdownpanel('destroy');
        start();
    }, 400);

});


test("show and show again", function () {
    stop();
    expect(3);

    // create, and see that is is not visible
    $('#the-node').pushdownpanel({
    });
    equal($('#the-node').is(':visible'), false);
    
    // show it
    $('#the-node').pushdownpanel('show');

    // wait for animation finished
    setTimeout(function () {
        equal($('#the-node').is(':visible'), true);

        // show it again (nothing happens)
        $('#the-node').pushdownpanel('show');

        equal($('#the-node').is(':visible'), true);

        $('#the-node').pushdownpanel('destroy');
        start();
    }, 400);

});


test("hide while showing", function () {
    stop();
    expect(2);

    // create, and see that is is not visible
    $('#the-node').pushdownpanel({
    });
    equal($('#the-node').is(':visible'), false);
    
    // show it
    $('#the-node').pushdownpanel('show');

    // hide it (will be ignored... as it is
    // during a state change.)
    $('#the-node').pushdownpanel('hide');

    // wait for animation finished
    setTimeout(function () {
        equal($('#the-node').is(':visible'), true);
        $('#the-node').pushdownpanel('destroy');
        start();
    }, 400);

});


test("show while hiding", function () {
    stop();
    expect(3);

    // create, and see that is is not visible
    $('#the-node').pushdownpanel({
    });
    equal($('#the-node').is(':visible'), false);
    
    // show it
    $('#the-node').pushdownpanel('show');

    // wait for animation finished
    setTimeout(function () {
        equal($('#the-node').is(':visible'), true);

        // hide it
        $('#the-node').pushdownpanel('hide');

        // show it (ignored, as we are in state change)
        $('#the-node').pushdownpanel('show');

        setTimeout(function () {
            equal($('#the-node').is(':visible'), false);
            $('#the-node').pushdownpanel('destroy');
            start();
        }, 400);

    }, 400);

});


test("hide while hiding", function () {
    stop();
    expect(3);

    // create, and see that is is not visible
    $('#the-node').pushdownpanel({
    });
    equal($('#the-node').is(':visible'), false);
    
    // show it
    $('#the-node').pushdownpanel('show');

    // wait for animation finished
    setTimeout(function () {
        equal($('#the-node').is(':visible'), true);

        // hide it
        $('#the-node').pushdownpanel('hide');

        // hide it again
        $('#the-node').pushdownpanel('hide');

        setTimeout(function () {
            equal($('#the-node').is(':visible'), false);
            $('#the-node').pushdownpanel('destroy');
            start();
        }, 200);

    }, 400);

});


test("hide and hide again", function () {
    stop();
    expect(4);

    // create, and see that is is not visible
    $('#the-node').pushdownpanel({
    });
    equal($('#the-node').is(':visible'), false);
    
    // show it
    $('#the-node').pushdownpanel('show');

    // wait for animation finished
    setTimeout(function () {
        equal($('#the-node').is(':visible'), true);

        // hide it
        $('#the-node').pushdownpanel('hide');

        setTimeout(function () {
            equal($('#the-node').is(':visible'), false);

            // hide it again
            $('#the-node').pushdownpanel('hide');

            setTimeout(function () {
                equal($('#the-node').is(':visible'), false);
                $('#the-node').pushdownpanel('destroy');
                start();
            }, 200);
        }, 200);

    }, 400);

});


test("trigger events beforeShow, show, beforeHide, hide", function () {
    stop();
    expect(8);

    var events = [];
    function markEvent(evt) {
        events.push(evt.type);
    }

    // create, and see that is is not visible
    $('#the-node').pushdownpanel({
        beforeShow: markEvent,
        show: markEvent,
        beforeHide: markEvent,
        hide: markEvent
    });
    equal($('#the-node').is(':visible'), false);
    same(events, []);

    // show it
    $('#the-node').pushdownpanel('show');
    same(events, ['pushdownpanelbeforeshow']);

    // wait for animation finished
    setTimeout(function () {
        equal($('#the-node').is(':visible'), true);
        same(events, 
            ['pushdownpanelbeforeshow', 'pushdownpanelshow']);

        // hide it
        $('#the-node').pushdownpanel('hide');
        same(events,
            ['pushdownpanelbeforeshow', 'pushdownpanelshow',
            'pushdownpanelbeforehide']);

        setTimeout(function () {
            equal($('#the-node').is(':visible'), false);
            same(events,
                ['pushdownpanelbeforeshow', 'pushdownpanelshow',
                'pushdownpanelbeforehide', 'pushdownpanelhide']);
            $('#the-node').pushdownpanel('destroy');
            start();
        }, 200);
    }, 400);

});


test("showing a pushdown hides all the others", function () {
    stop();
    expect(5);

    // need some more
    $('#main').append(
        '<div id="second-node">And now for something completely different</div>'
    );

    // create, and see that is is not visible
    $('#the-node').pushdownpanel({
    });
    $('#second-node').pushdownpanel({
    });
    equal($('#the-node').is(':visible'), false);
    equal($('#second-node').is(':visible'), false);
    
    // show it
    $('#the-node').pushdownpanel('show');

    // wait for animation finished
    setTimeout(function () {
        equal($('#the-node').is(':visible'), true);

        // Show the second one
        $('#second-node').pushdownpanel('show');

        setTimeout(function () {
            // second is shown
            equal($('#second-node').is(':visible'), true);
            // first is hidden
            equal($('#the-node').is(':visible'), false);

            $('#the-node').pushdownpanel('destroy');
            $('#second-node').pushdownpanel('destroy');
            start();
        }, 400);

    }, 400);

});


