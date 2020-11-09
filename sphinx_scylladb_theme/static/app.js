$(document).ready(function() {
    $(window).on('resize', Foundation.utils.throttle(function (e) {
        if (Foundation.utils.is_small_only()) {
            $('.topbar_continer').removeClass('contain-to-grid');
        } else {
            $('.topbar_continer').addClass('contain-to-grid')
        }
    }, 300));
});

// Opens external links in a new tab
$(document).ready(function () {
    const isExternal = new RegExp('^(?:[a-z]+:)?//', 'i');
    $('a.reference').each(function() {
        $(this).removeClass('internal external');

        if (isExternal.test($(this).attr('href'))) {
            $(this).addClass('external');
            $(this).attr('target', '_blank')
        } else {
            $(this).addClass('internal');
        }
    });  
});

