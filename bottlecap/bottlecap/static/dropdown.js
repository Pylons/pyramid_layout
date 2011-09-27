/*globals jQuery:false  */
(function ($) {

    function clearMenus() {
        $('a.menu, .dropdown-toggle').parent('li').removeClass('open');
    }

    $(function () {
        $('html').bind("click", clearMenus);
        $('body').dropdown('[data-dropdown] a.menu, [data-dropdown] .dropdown-toggle');
    });

    $.fn.dropdown = function (selector) {
        return this.each(function () {
            $(this).delegate(selector || 'a.menu, .dropdown-toggle', 'click', function (e) {
                var li = $(this).parent('li');
                clearMenus();
                li.toggleClass('open');
                return false;
            });
        });
    };

}(jQuery));