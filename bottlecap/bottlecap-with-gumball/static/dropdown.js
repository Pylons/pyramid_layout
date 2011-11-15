/*globals jQuery:false  */
(function ($) {

    var d = '.quickpanel-toggle';
    function clearMenus() {
        $(d).removeClass('open');
    }
    $(function () {
        $('#navigation-toggle').add('#search-toggle').bind('click touchstart', function (e) {
            var isActive = $(this).hasClass('open');
            clearMenus();
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
    
}(jQuery));