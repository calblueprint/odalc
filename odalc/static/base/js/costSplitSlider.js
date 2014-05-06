var MAX_AMT = 20.00;

var calculateAmount = function(perc) {
    return perc/100 * MAX_AMT + 5;
};

var percentageToDollar = function(perc) {
    return calculateAmount(perc).toFixed(2);
};

var percentageOfDollar = function(costPerc, perc) {
    return (calculateAmount(costPerc) * perc / 100).toFixed(2);
};

var calculateYourAmt = function(costPerc, perc) {
    return (percentageToDollar(costPerc) - percentageOfDollar(costPerc, perc)).toFixed(2);
};

$().ready(function() {
    $('#cost-dollar-amt').text('$' + percentageToDollar(parseInt($('#cost-slider').val())));
    $('#split-dollar-amt').text('$' + percentageOfDollar(
        parseInt($('#cost-slider').val()),
        parseInt($('#split-slider').val())
    ));
    $('#your-amt').text('$' + calculateYourAmt(
        parseInt($('#cost-slider').val()),
        parseInt($('#split-slider').val())
    ));

    // update actual form elements
    $(formCostId).val(percentageToDollar(
        parseInt($('#cost-slider').val())
    ));
    $(formOdalcSplitId).val(percentageOfDollar(
        parseInt($('#cost-slider').val()),
        parseInt($('#split-slider').val())
    ));


    // Event handler when cost amount is adjusted
    $('#cost-dollar-amt').on('mousedown mousemove', function() {
        $('body').on('mousemove', function() {
            // update UI elements
            $('#cost-dollar-amt').text('$' + percentageToDollar(parseInt($('#cost-slider').val())));
            $('#split-dollar-amt').text('$' + percentageOfDollar(
                parseInt($('#cost-slider').val()),
                parseInt($('#split-slider').val())
            ));
            $('#your-amt').text('$' + calculateYourAmt(
                parseInt($('#cost-slider').val()),
                parseInt($('#split-slider').val())
            ));

            // update actual form elements
            $(formCostId).val(percentageToDollar(
                parseInt($('#cost-slider').val())
            ));
            $(formOdalcSplitId).val(percentageOfDollar(
                parseInt($('#cost-slider').val()),
                parseInt($('#split-slider').val())
            ));

        });
    });

    // Event handler for when split amount is adjusted
    $('#split-dollar-amt').on('mousedown mousemove', function() {
        $('body').on('mousemove', function() {
            // update UI elements
            $('#split-dollar-amt').text('$' + percentageOfDollar(
                parseInt($('#cost-slider').val()),
                parseInt($('#split-slider').val())
            ));
            $('#your-amt').text('$' + calculateYourAmt(
                parseInt($('#cost-slider').val()),
                parseInt($('#split-slider').val())
            ));

            // update actual form elements
            $(formOdalcSplitId).val(percentageOfDollar(
                parseInt($('#cost-slider').val()),
                parseInt($('#split-slider').val())
            ));
        });
    });

});
