/*globals jQuery:false  */
(function ($) {
   
    $(function () {
        $('body').quickpanel('.dropdown-toggle');
    });

    $.fn.quickpanel = function (selector) {
        return this.each(function () {
            $(this).delegate(selector, 'click', function (e) {
                var $par = $(this).parents('[data-quickpanel="quickpanel"]');
                $('[data-quickpanel]').not($par).removeClass('open');
                $par.toggleClass('open');
                if(e.currentTarget.id === 'search-toggle') {
                    $par.find('.search-site-box').focus();
                }
                return false;
            });
        });
    };
    
}(jQuery));