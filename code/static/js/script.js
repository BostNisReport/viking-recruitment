$().ready(function() {
    $(".datepicker").datepicker({
        format: "dd-mm-yyyy"
    });

    //selectpicker
    $('.selectpicker').selectpicker();

    //partner checkbox
    $('#partnerCheckbox').click(function() {
        if($(this).is(':checked')) {
            $('#inputPartner').prop('disabled', false);
        } else {
            $('#inputPartner').prop('disabled', true);
        }
    });

    //section hide/show
    $('.close-section').click(function() {
        $(this).parent().parent().children('*').toggle();
        $(this).parent().parent().toggleClass('hidden');
        $(this).parent().show();

        if($(this).text() == 'Hide') {
            $(this).text('Show');
        } else {
            $(this).text('Hide');
        }

        return false;
    });

    $(".apply-btn").on("click", function() {
        $(this).html("Applied");
    });
});
