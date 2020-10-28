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
  $('a.reference').each(function() {
    var href = $(this).attr('href');
    var isExternal = new RegExp('^(?:[a-z]+:)?//', 'i');
    $(this).removeClass('internal external');
    
    if (isExternal.test(href)) {
        $(this).addClass('external');
        $(this).attr('target', '_blank')
    } else {
        $(this).addClass('internal');
    }
  });  
});

