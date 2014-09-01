var MAX_AMT = 50.00;
var MIN_DONATE_PERCENT = 0.2;

var percentageToDollar = function(perc, maxAmt) {
    return ((perc/100) * maxAmt).toFixed(2);
};

var calculatePercentage = function(cost, perc) {
    return (cost - percentageToDollar(perc, cost)).toFixed(2);
}

$('[data-slider]').on('change', function(){
    $('#donate-amt-box').val($('#donate-amt').attr('data-slider'));
});

    // Event handler for when split amount is adjusted
$('#split-dollar-slider').on('mousedown mousemove', function() {
    $('body').on('mousemove', function() {
        // update UI elements
        $('#split-dollar-amt').text('$' + calculatePercentage(
            parseFloat($('#id_cost').val()),
            100 - parseInt($('#split-slider').val())
        ));

        $('#your-amt').text('$' + calculatePercentage(
            parseFloat($('#id_cost').val()),
            parseInt($('#split-slider').val())
        ));

        $('#dollar-handle').text($('#split-slider').val() + '%');

        // update actual form elements
        $('#id_odalc_cost_split').val(
            parseFloat($('#split-dollar-amt').text().slice(1))
        );
    });
});
