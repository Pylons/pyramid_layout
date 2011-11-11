/*jslint browser: true */
/*global jQuery: false, console: false, window: false, Modernizr:false */

/* Gumball javascript */

(function ($) {

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
    
    $('nav.search select').change(function () {
        $(this).prev().text($('option[value="' +this.value + '"]', this).text());
    });

} (jQuery));
