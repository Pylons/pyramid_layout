
/*jslint undef: true, newcap: true, nomen: false, white: true, regexp: true */
/*jslint plusplus: false, bitwise: true, maxerr: 50, maxlen: 80, indent: 4 */
/*jslint sub: true */
/*globals window navigator document console */
/*globals setTimeout clearTimeout setInterval */ 
/*globals jQuery Mustache */


(function ($) {

    var log = function () {
        if (window.console && console.log) {
            // log for FireBug or WebKit console
            console.log(Array.prototype.slice.call(arguments));
        }
    };

    function isoDate(d) {
        return d.getUTCFullYear() + '-' + (d.getUTCMonth() + 1) +
            '-' + d.getUTCDate() + 'T' + d.getUTCHours() + ':' +
            d.getUTCMinutes() + ':' + d.getUTCSeconds();
    }

    
    $.widget('popper.pushdowntab', {
        // This component is responsible for managing the tab of
        // the pushdown. Clicking on the tab opens and closes the
        // pushdown, the click event will be bound here.
        //
        // The pushdown panel component is encapsulated
        // and created by pushdowntab, so it needs not to be touched
        // directly.
        //
        // Another responsibility of this widget is to handle the
        // update of the "recent items counter", in cooperation
        // with the popper.notifier component that broadcasts the
        // notifications streamed from the server, as well as remembers
        // the last update timestamp for each notification source.

        options: {
            name: null,  // a unique name that identifies this pushdown
            selectTopBar: null,  // selector for the top bar.
                                 // The panel will be inserted after this.
            findCounterLabel: null,   // find the label for the recent items
                                 //  (inside the widget's bound element)

            fullWindow: false
            //beforeShow: function(evt) {},    // onBeforeShow event handler
            //show: function(evt) {},    // onShow event handler
            //beforeHide: function(evt) {},    // onBeforeHide event handler
            //hide: function(evt) {}    // onHide event handler
        },

        getCounter: function () {
            var cnt = this.counterlabel.text();
            cnt = Math.floor(Number(cnt) || 0);
            if (cnt < 0) {
                cnt = 0;
            }
            return cnt;
        },

        setCounter: function (cnt) {
            this.counterlabel.text('' + cnt);
            if (cnt > 0) {
                this.counterlabel.show();
            } else {
                this.counterlabel.hide();
            }
        },


        // --
        // private parts
        // --
        
        _create: function () {
            var self = this;
            // initialize the panel
            this.panel = $('<div></div>')
                .attr('id', 'popper-pushdown-' + this.options.name)
                .insertAfter($(this.options.selectTopBar))
                .pushdownpanel({
                    fullWindow: this.options.fullWindow,
                    selectTopBar: this.options.selectTopBar,
                    beforeShow: $.proxy(this._onBeforeShow, this),
                    show: $.proxy(this._onShow, this),
                    beforeHide: $.proxy(this._onBeforeHide, this),
                    hide: $.proxy(this._onHide, this)
                });
            // make us clickable
            this.element.click($.proxy(this._onClick, this));
            // markers
            this.counterlabel =
                this.element.find(this.options.findCounterLabel);
            // Listen for counter updates
            $(document).bind('notifierUpdate',
                $.proxy(this._onNotifierUpdate, this));
        },

        _destroy: function () {
            this.panel.pushdownpanel('destroy');
            this.element.unbind('click');
            $(document).unbind('notifierUpdate',
                $.proxy(this._onNotifierUpdate, this));
        },

        // handle click on tab link
        _onClick: function (evt) {
            this.panel.pushdownpanel('toggle');
            return false;
        },

        // handle panel event
        _onBeforeShow: function (evt) {
            this._trigger('beforeShow', evt);

            // XXX XXX Will want proper ajax here.
            // Currently just use the fake data.
            var head_data = window.head_data || {};
            var microtemplates = head_data.microtemplates || {};
            var panel_data = head_data.panel_data || {};
            var template = microtemplates[this.options.name];
            var data = panel_data[this.options.name];
            if (template === undefined) {
                throw new Error('bc.microtemplate: "' + this.options.name +
                    '" template does not exist in head_data.microtemplates.');
            }

            // Render the template.
            var html = Mustache.to_html(template, data);
            this.panel.html(html);
            // Reset the counter.
            // We also have to remember to ask the next update
            // starting from this moment.
            this.setCounter(0);
            var now = new Date();
            $(document).trigger('notifierSetTs', [this.options.name, now]);
        },

        // handle panel event
        _onShow: function (evt) {
            this._trigger('show', evt);
        },

        // handle panel event
        _onBeforeHide: function (evt) {
            this._trigger('beforeHide', evt);
        },

        // handle panel event
        _onHide: function (evt) {
            this._trigger('hide', evt);
        },

        // handle notifier event
        _onNotifierUpdate: function (evt, updates) {
            var info = updates[this.options.name];
            // Is there an update that belongs to me?
            if (info !== undefined) {
                log('pushdown ' + this.options.name +
                    ' updating with: ' + info.cnt);
                // What is the state currently?
                var panel = this.panel.data('pushdownpanel');
                if (panel.state == panel._STATES.HIDDEN ||
                        panel.state == panel._STATES.TO_HIDDEN) {
                    // Hidden state: add the counter, and update.
                    var counter = this.getCounter();
                    counter += info.cnt;
                    this.setCounter(counter);
                }
                // (Visible state. Nothing to do. In this case:
                // we will reset when we go to hidden.)
            }
        }


    });


    $.widget('popper.pushdownpanel', {
        // Pushdown animation
        // This component is responsible for showing and hiding
        // the "pushdown" panel,
        // animating it, and updating its content. 

        options: {
            fullWindow: true,
            selectTopBar: null  // selector for the top bar.
                // It is _only_ used if fullWindow is false,
                // to calculate height for the pushdown.
                // XXX, could we do without this?

            //beforeShow: function(evt) {},    // onBeforeShow event handler
            //show: function(evt) {},    // onShow event handler
            //beforeHide: function(evt) {},    // onBeforeHide event handler
            //hide: function(evt) {}    // onHide event handler
        },

        show: function (callback) {
            var self = this, this_height;
            if (this.state != this._STATES.HIDDEN) {
                // Ignore it if we are not showable.
                if (callback) {
                    callback();
                }
            } else {
                // Show it.
                this.state = this._STATES.TO_VISIBLE;
                this._trigger('beforeShow', null);
                this.element.show();
                var height;
                // XXX Will need some cleanup here
                // XXX to produce desired height in a solid way.
                if (this.options.fullWindow) {
                    height = ($(window).height() - 50) - 
                        ($(this.options.selectTopBar).height() * 2);
                } else {
                    this.element.css('height', '100%');
                    height = this.element.height();
                }
                this.element.height(0);
                this.element
                    .animate({
                        height: height
                    }, 350, function () {
                        self.state = self._STATES.VISIBLE;
                        if (callback) {
                            callback();
                        }
                        self._trigger('show', null);
                    });
                
            }
            // allow chaining
            return this;
        },

        hide: function (callback) {
            var self = this;
            if (this.state != this._STATES.VISIBLE) {
                // Ignore it if we are not hidable.
                if (callback) {
                    callback();
                }
            } else {
                // Hide it.
                this.state = this._STATES.TO_HIDDEN;
                this._trigger('beforeHide', null);
                this.element
                    .animate({
                        height: 0
                    }, 150, function () {
                        self.state = self._STATES.HIDDEN;
                        self.element.hide();
                        if (callback) {
                            callback();
                        }
                        self._trigger('hide', null);
                    });
            }
            // allow chaining
            return this;
        },

        toggle: function (callback) {
            if (this.state == this._STATES.VISIBLE) {
                this.hide(callback);
            } else if (this.state == this._STATES.HIDDEN) {
                this.show(callback);
            } else {
                // Ignore it if we are transitioning.
                if (callback) {
                    callback();
                }
            }
            // allow chaining
            return this;
        },


        // --
        // private parts
        // --
        

        _STATES: {
            HIDDEN: 0,
            TO_VISIBLE: 1,
            VISIBLE: 2,
            TO_HIDDEN: 3
        },

        _create: function () {
            var self = this;
            // initialize the content to hidden
            this.state = this._STATES.HIDDEN;
            this.element.hide();
            // If any other pushdown opens, we have to close.
            // So, we listen on the document where all events will bubble up.
            $(document).bind('pushdownpanelbeforeshow',
                $.proxy(this._onBeforeShowAny, this));
        },

        _destroy: function () {
            $(document).unbind('pushdownpanelbeforeshow',
                $.proxy(this._onBeforeShowAny, this));
        },

        _onBeforeShowAny: function (evt) {
            // Is this the event that we ourselves have triggered?
            if (evt.target == this.element[0]) {
                // Right, don't close ourselves, as we are the one opening
                return;
            }
            // Some other pushdown opened, so close me.
            this.hide();
        }

    });


    $.widget('popper.notifier', {
        // A singleton component that ought to be bound to the document.
        // It fetches all notifications from the server, and broadcasts
        // the notifications streamed from the server. It also remembers
        // the last update timestamp for each notification source.

        options: {
            url: null,    // url for ajax
            polling: 120  // polling time in seconds (!!)
        },


        // --
        // private parts
        // --
        
        _create: function () {
            var self = this;
            // Start the timer
            this.timer = setInterval(
                $.proxy(this._poll, this),
                this.options.polling * 1000
            );
            // Empty request
            this.xhr = null;
            // the recent updates
            this.updates = {};

            // listen to an event to set the timestamp
            $(document).bind('notifierSetTs',
                $.proxy(this._onSetTs, this));
        },

        _destroy: function () {
            clearTimeout(this.timer);
            if (this.xhr) {
                this.xhr.abort();
            }
            this.xhr = null;
            $(document).unbind('notifierSetTs',
                $.proxy(this._onSetTs, this));
        },

        // timed handler
        _poll: function () {
            if (this.xhr) {
                this.xhr.abort();
            }
            this.xhr = $.ajax({
                url: this.options.url,
                data: this.updates,
                type: 'GET'
            });
            this.xhr
                .done($.proxy(this._ajaxDone, this))
                .error($.proxy(this._ajaxError, this));
        },

        // Allows the pushdown to set their ts if they want
        // this means a pushdown is up-to-date till this moment.
        _onSetTs: function (evt, name, d) {
            log('setTs', name, d);
            // Update the timestamp for a given date.
            this.updates[name] = isoDate(d);
        },


        // handle ajax response
        _ajaxDone: function (result) {
            var self = this;
            if (! result || result.error) {
                // Allow IE to return no payload as success,
                // (to prepare for foul outcomes such as aborts on the
                // non standard browsers),
                // as well as, our view can return {error='Display me!'} to
                // signify an express error condition inside a 200 response.
                return this._ajaxError(this.xhr, result.error || 'FATAL');
            }
            // Remember our recent updates.
            $.each(result, function (name, value) {
                self.updates[name] = value.ts;
            });
            // Notify everyone who is interested.
            $(document).trigger('notifierUpdate', [result]);
        },

        // handle ajax response
        _ajaxError: function (xhr, textStatus) {
            log('Notifier ajax: We will do something with this, ' + textStatus);
        }

    });


})(jQuery);
