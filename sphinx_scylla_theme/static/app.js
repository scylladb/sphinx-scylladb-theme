$(document).ready(function() {
    $(window).on('resize', Foundation.utils.throttle(function (e) {
        if (Foundation.utils.is_small_only()) {
            $('.topbar_continer').removeClass('contain-to-grid');
        } else {
            $('.topbar_continer').addClass('contain-to-grid')
        }
    }, 300));
});
