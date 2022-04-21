function validate_required() {
    let valid = true;
    $('input,textarea,select').filter('[required]:visible').each(function (i, requiredField) {
        if ($(requiredField).val() === '') {
            $(requiredField).addClass('border-danger').removeClass("form-control-alternative");
            valid = false;
        } else {
            $(requiredField).removeClass('border-danger').addClass("form-control-alternative");
        }
    });
    return valid;
}
