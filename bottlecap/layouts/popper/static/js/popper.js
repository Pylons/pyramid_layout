/*jslint browser: true */
/*global jQuery: false, console: false, window: false, Modernizr:false, yepnope: false, radarlink: true, Mustache: false */

$(function () {
    // Slide down the global site-wide notification
    setTimeout( 
        function () {
            $('.globalNotification').slideDown('medium');
        }, 1000);
}(jQuery));

/* Gumball javascript */

(function ($) {

    if(Modernizr.prefixed('boxSizing')) {
        $('html').addClass('boxsizing');
    }

    var log = function () {
            if (window.console && console.log) {
                // log for FireBug or WebKit console
                console.log(Array.prototype.slice.call(arguments));
            }
        },
        initWidth = document.documentElement.clientWidth;

    // polyfill for the borwsers not supporting the 'placeholder' attribute
    if (!Modernizr.input.placeholder) {
        $("input, textarea").each(function () {
            if ($(this).val() === "" && $(this).attr("placeholder") !== "") {
                $(this).val($(this).attr("placeholder"));
                $(this).focus(function () {
                    if ($(this).val() === $(this).attr("placeholder")) {
                        $(this).val("");
                    }
                });
                $(this).blur(function () {
                    if ($(this).val() === "") {
                        $(this).val($(this).attr("placeholder"));
                    }
                });
            }
        });

        $("form").submit(function () {
            $("input, textarea").each(function () {
                if ($(this).attr("placeholder") !== "") {
                    if ($(this).val() === $(this).attr("placeholder")) {
                        $(this).val("");
                    }
                }
            });
        });
    }
    
    // Add nice-looking spans to cover the standard <select> elements in the search
    if(!$('html').hasClass('oldie')) {
        $('nav.search').find('select').each(function () {
            var $that = $(this);
            $that.after('<span class="fieldCoverage">' + this[0].text + '</span>');
            $that.change(function () {
                $that.prev().text($('option:selected', $that).text());
            });
            
        });    
    }
       
    // bind community filter click event to location change
    $('#filter-options input').click(function() {window.location=this.value;});
 
    $('nav.search select').change(function () {
        $(this).next().text($('option[value="' +this.value + '"]', this).text());
    });
    
    $('#tags').tagbox({});

    // Global notification dismissing
    $('.dismissNotification').click(function () {
        $(this).parent().slideUp('fast');
    });
    
    
    // Reveal the search options on :focus
    var $fst = $('form#search-form fieldset');
    $fst.find('.search-site-box')
        .focusin(function () {
            if (Modernizr.csstransitions && !$fst.hasClass('opened')) {
                $fst.addClass('opened');
            } else if (!Modernizr.csstransitions && !$fst.hasClass('opened')){
                $fst.animate({
                    marginTop: '.2em'
                }, 4000);            
            }
        });

    // --
    // Component for expanding panels
    // --
    

    $.widget('bc.microtemplate', {

        options: {
            //name: ''           // name of the microtemplate
        },

        render: function(data) {
            var rendered = this._rendered(data);
            this.element.html(rendered);
            // allow chaining
            return this;
        },


        // --
        // private parts
        // --
        

        _create: function() {
            var self = this;
            if (! (this.options.name && this.options.name.length > 0)) {
                throw new Error('bc.microtemplate: "name" option is mandatory.');
            }
        },


        //destroy: function() {
        //    // In jQuery UI 1.8, you must invoke the destroy method from the base widget
        //    $.Widget.prototype.destroy.call( this );
        //    // In jQuery UI 1.9 and above, you would define _destroy instead of destroy and not call the base method
        //}
        
        _rendered: function(data) {
            var head_data = window.head_data || {};
            var microtemplates = head_data.microtemplates || {};
            var template = microtemplates[this.options.name];
            if (template === undefined) {
                throw new Error('bc.microtemplate: "' + this.options.name + '" template does not exist in head_data.microtemplates.');
            }

            // Render the template.
            var html = Mustache.to_html(template, data);

            return html;
        }

    });


    $.widget('bc.expandpanel', {

        options: {
            fullWindow: false
            //beforeShow: function(evt) {},    // onBeforeShow event handler
            //show: function(evt) {},    // onShow event handler
            //beforeHide: function(evt) {},    // onBeforeHide event handler
            //hide: function(evt) {}    // onHide event handler
        },

        show: function(callback) {
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
                this.element.slideDown('350', function() {
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

        hide: function(callback) {
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
                this.element.slideUp('150', function() {
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

        toggle: function(callback) {
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

        _create: function() {
            var self = this;
            // initialize the content to hidden
            this.state = this._STATES.HIDDEN;
            this.element.hide();
        }

        //destroy: function() {
        //    // In jQuery UI 1.8, you must invoke the destroy method from the base widget
        //    $.Widget.prototype.destroy.call( this );
        //    // In jQuery UI 1.9 and above, you would define _destroy instead of destroy and not call the base method
        //}


    });


    // --
    // Wire chatterpanel in header
    // --
    
    $(function() {

        function closeAllPanels() {
            // temporary solution here
            $('.expanding-panel').expandpanel('hide');
        }


        var head_data = window.head_data || {},
            chatterLink, radarLink;

        var microtemplateChatter = $('<div id="microtemplate-chatter" class="expanding-panel"></div>')
            .insertAfter('#top-bar')
            .microtemplate({
                name: 'chatter'
                })
            .expandpanel({
                beforeShow: function(evt) {
                    chatterLink.parent().addClass('selectedPushDown');
                },
                hide: function(evt) {
                    chatterLink.parent().removeClass('selectedPushDown');
                }
        });
        

        var chatterData = head_data.panel_data.chatter;
        log('preload data for chatter panel:', chatterData);

        chatterLink = $('a#chatter')
            .click(function() {
                closeAllPanels();
                microtemplateChatter
                    .microtemplate('render', chatterData)
                    .expandpanel('toggle');
                    
                    // just an emulation. In production this should be initialized by the start of the AJAX call to the server
                    setTimeout(function() {
                        // show the 'loading' icon
                        // IMPORTANT! This needs to be updated to work with the real data instead of mocking it
                        $('.updating')
                            .animate({
                                opacity: '1'
                            },100)
                            .delay(5000)
                            .animate({
                                opacity: '0'
                            }, 100, function () {
                                var houstonWeHaveAProblem = true;
                                // Emulate the problem with connecting to the server
                                if (houstonWeHaveAProblem) {
                                    $('.houstonWeHaveAProblem')
                                        .fadeIn(100)
                                        .delay(3000);
                                }
                            });
                    }, 3000);
                    
                return false;
            });


        // chatter options toggling
        //
        //var chatterOptionsPanel = $('#chatter-options-panel')
        //    .expandpanel({
        //    });
        //var chatterOptionsLink = $('#chatter-options-link')
        //    .click(function() {
        //        log('XXX')
        //        chatterOptionsPanel.expandpanel('toggle');
        //        return false;
        //    });

        var chatterOptionsPanel = $('.chatter-options-link')
            .live('click', function(e) {
                var el = $(this);
                var panel = el.parent().find('.chatter-options-panel');
                if (panel.css('opacity') != '1') {
                    panel.css('opacity', '1');
                } else {
                    panel.css('opacity', '0');
                }
                e.preventDefault();
            });

        var microtemplateRadar = $('<div id="microtemplate-radar" class="expanding-panel"></div>')
            .insertAfter('#top-bar')
            .microtemplate({
                name: 'radar'
                })
            .expandpanel({
                fullWindow: true,
                beforeShow: function(evt) {
                    radarLink.parent().addClass('selectedPushDown');
                },
                hide: function(evt) {
                    radarLink.parent().removeClass('selectedPushDown');
                }
        });

        var radarData = head_data.panel_data.radar;
        log('preload data for radar panel:', radarData);

        radarLink = $('a#radar')
            .click(function() {
                closeAllPanels();
                microtemplateRadar
                    .microtemplate('render', radarData)
                    .expandpanel('toggle');
                return false;
            });

    });


} (jQuery));
