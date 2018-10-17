$(document).ready(main);

var SUBMIT_ALLOWED;

function main(){
    SUBMIT_ALLOWED = false;
    $('#login-email-input').change(validateEmail);
    $('#login-password-input').change(function(){
       resetDefault($(this));
    });
    $('#login-submit').click(confirmSubmitAllowed);
    var loginError = $('.login-error-block');
    if(loginError.length > 0){
        console.log('login error log');
        setTimeout(function(){
            loginError.slideUp(500);
        }, 5000)
    }
}

function resetDefault(item){
    item.removeClass('is-valid');
    item.removeClass('is-invalid');
}

function confirmSubmitAllowed(event){
    if(!SUBMIT_ALLOWED){
        event.preventDefault();
    }
}

function validateEmail(){

    function informUser(response){
        var emailInput = $('#login-email-input');
        resetDefault(emailInput);
        if(response.existence){
            emailInput.addClass('is-valid');
            SUBMIT_ALLOWED = true
        }
        else{
            emailInput.addClass('is-invalid');
            SUBMIT_ALLOWED = false
        }
    }

    var email = $(this).val();
    $.ajax({
        url: '/accounts/ajax_validateEmail',
        method: 'GET',
        data: {'email': email},
        dataType: 'json',
        success: informUser
    })
}