/*globals jQuery:false  */
(function ($) {

    function clearMenus() {
        $('[data-quickpanel]').removeClass('open');
    }

    $(function () {
        $('html.no-touch').bind("click", clearMenus);
        $('html.touch').bind("touchstart", clearMenus);        
        $('body').quickpanel('[data-quickpanel] .quickpanel-toggle');
        
        $('.touch .dropdown-toggle').bind('touchend', function (e) {
            $(this).parents('[data-quickpanel="dropdown"]').toggleClass('open');
            e.preventDefault();
        });
    });

    $.fn.quickpanel = function (selector) {
        return this.each(function () {
            $(this).delegate(selector, 'click', function (e) {
                var $li = $(this).parents('[data-quickpanel="quickpanel"]');
                $('[data-quickpanel]').not($li).removeClass('open');
                $li.toggleClass('open');
                return false;
            });
        });
    };

}(jQuery));