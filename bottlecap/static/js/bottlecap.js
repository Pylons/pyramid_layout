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
        keywordsList.append('<li><a href="#"><span class="keyword">'+ $('input[type="text"]', $(this)).val() +'</span><span class="keywordCounter"></span></a></li>');
        return false;
    });

} (jQuery));
