/*globals jQuery:false  */
(function ($) {

    $(function () {
        $('#navigation-toggle').add('#search-toggle').bind('click touchstart', function (e) {
            var isActive = $(this).hasClass('open');
            $('.quickpanel-toggle').removeClass('open');
            if (!isActive) {
                $(this).toggleClass('open');
                if(e.currentTarget.id === 'search-toggle') {
                    $('#search-site-box').focus();
                    $('#global-nav').toggleClass('notched');
                }
            }
            return false;
        });
    });
    
    $(function () {
        $('body').quickpanel('.quickpanel-toggle');
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