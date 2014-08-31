$(document).ready(function() {

    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#active-section").on('click', '.feature-course-button', function(){
        $(this).removeClass('feature-course-button').addClass('unfeature-course-button');
        $(this).parents(".course-row").prependTo('#featured-section');
        $(this).text("Remove from featured");

        var courseId = $(this).parents('.course-row').attr('id');
        $.ajax({
            type: 'POST',
            url: 'ajax/dashboard',
            data: {
                'courseId': courseId,
                'isFeatured': true,
            },
        });

        return false;
    });

    $("#featured-section").on('click', '.unfeature-course-button', function(){
        $(this).removeClass('unfeature-course-button').addClass('feature-course-button');
        $(this).parents(".course-row").prependTo('#active-section');
        $(this).text("Add to featured");

        var courseId = $(this).parents('.course-row').attr('id');
        $.ajax({
            type: 'POST',
            url: 'ajax/dashboard',
            data: {
                'courseId': courseId,
                'isFeatured': false,
            },
        });

        return false;
    });

});
