/*globals jQuery:false  */
(function ($) {

    function clearMenus() {
        $('[data-quickpanel]').removeClass('open');
    }

    $(function () {
        $('html').bind("click", clearMenus);
        $('body').quickpanel('[data-quickpanel] .quickpanel-toggle');
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