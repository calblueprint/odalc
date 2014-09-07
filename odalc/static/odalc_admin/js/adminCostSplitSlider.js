var percentageToDollar = function(perc, maxAmt) {
    return ((perc/100) * maxAmt).toFixed(2);
};

var calculatePercentage = function(cost, perc) {
    return (cost - percentageToDollar(perc, cost)).toFixed(2);
}


$().ready(function() {
    var cost = parseFloat($('#id_cost').val());
    var odalc_cost_split =  parseFloat($('#id_odalc_cost_split').val());
    var slider_val = Math.round((odalc_cost_split / cost) * 100);

    $('#split-dollar-amt').text('$' + odalc_cost_split.toFixed(2));

    $('#your-amt').text('$' + (cost - odalc_cost_split).toFixed(2));

    $('#split-slider-val').val(slider_val);
    $('#dollar-handle').text(slider_val + '%');
    $('#split-dollar-slider').attr('data-slider', slider_val);


    // Event handler for when split amount is adjusted
    $('#split-dollar-slider').on('mousedown mousemove', function() {

        $('body').on('mousemove', function() {
            // update UI elements
            $('#split-dollar-amt').text('$' + calculatePercentage(
                parseFloat($('#id_cost').val()),
                100 - parseInt($('#split-slider-val').val())
            ));

            $('#your-amt').text('$' + calculatePercentage(
                parseFloat($('#id_cost').val()),
                parseInt($('#split-slider-val').val())
            ));

            $('#dollar-handle').text($('#split-slider-val').val() + '%');

            // update actual form elements
            $('#id_odalc_cost_split').val(
                parseFloat($('#split-dollar-amt').text().slice(1))
            );
        });
    });
});
