$(document).ready(function() {
    var max_fields      = 10; //maximum input boxes allowed
    var wrapper         = $(".prereq_fields_wrap"); //Fields wrapper
    var add_button      = $(".add_prereq_button"); //Add button ID

    var prereq_count = 1; //initlal text box count
    $(add_button).click(function(e){ //on add input button click
        e.preventDefault();
        if(prereq_count < max_fields){ //max input box allowed
            prereq_count++; //text box increment
            $(wrapper).append(
                '<div class="row collapse input-row">\
                    <div class="small-11 columns">\
                        <input type="text" name="prereq_fields[]"/>\
                    </div>\
                    <div class="small-1 columns">\
                        <a href="#" class="button alert postfix remove_field">&#x2715;</a>\
                    </div>\
                </div>'
            ); //add input box
        }
    });

    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault();
        $(this).parents('.input-row').remove();
        prereq_count--;
    })
});
