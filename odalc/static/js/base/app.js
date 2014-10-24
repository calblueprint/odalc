$(document).foundation();

// Make form tooltips appear on focus instead of hover
$(':input').on('focus', function(event) {
    $(this).prev('.has-tip').mouseenter();
}).on('blur', function(event) {
    $(this).prev('.has-tip').mouseout();
});
