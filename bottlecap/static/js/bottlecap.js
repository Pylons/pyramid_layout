/*jslint browser: true */
/*global jQuery: false, console: false, window: false, Modernizr:false */

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
    };

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
        $('nav.search select').each(function () {
            var $that = $(this);
            $(this).after('<span class="fieldCoverage">' + this[0].text + '</span>');
            $(this).change(function () {
                $(this).prev().text($('option:selected', $(this)).text());
            });
            
        });    
    }
        
    $('nav.search select').change(function () {
        $(this).next().text($('option[value="' +this.value + '"]', this).text());
    });
    
    $('form.addKeyword').bind('submit', function (e) {
        var keywordsList = $(this).prev('ul.keywords');
        keywordsList.append('<li><a href="#"><span class="keyword">'+ $('input[type="text"]', $(this)).val() +'</span><span class="keywordCounter">1</span></a></li>');
        return false;
    });



    // --
    // Component for Chatter
    // --

    $.widget('bc.chatterpanel', {

        options: {
            container: 'body',
            insertMethod: 'insertAfter'
        },

        show: function(callback) {
            var self = this;
            if (this.state != this._STATES.HIDDEN) {
                // Ignore it if we are not showable.
                if (callback) {
                    callback();
                }
            } else {
                // Show it.
                this.state = this._STATES.TO_VISIBLE;
                this.element.show();
                this.element.css('height', '100%');
                var height = this.element.height();
                this.element.height(0);
                this.element
                    .animate({
                        height: height
                    }, 350, function() {
                        self.state = self._STATES.VISIBLE;
                        if (callback) {
                            callback();
                        }
                    });
                
            }
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
                this.element
                    .animate({
                        height: 0
                    }, 150, function() {
                        self.state = self._STATES.HIDDEN;
                        self.element.hide();
                        if (callback) {
                            callback();
                        }
                    });
            }
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
            // Fill in the content for now. We will want this to
            // come from a microtemplate.
            // For now, we just reposition the tag to the
            // position as specified in the container option.
            var content = this.options.content;
            this.element[this.options.insertMethod](this.options.container);
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
        $('#chatter-panel').chatterpanel({
            container: '#top-bar'
        });

        $('#chatter').click(function() {
            $('#chatter-panel').chatterpanel('toggle');
            return false;
        });
    });


} (jQuery));
