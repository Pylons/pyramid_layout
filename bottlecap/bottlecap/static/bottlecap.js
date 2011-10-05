/*jslint browser: true */
/*global jQuery: false, console: false, window: false */

/* Gumball javascript */

(function ($) {

    var log = function () {
        if (window.console && console.log) {
            // log for FireBug or WebKit console
            console.log(Array.prototype.slice.call(arguments));
        }
    };

}(jQuery));
