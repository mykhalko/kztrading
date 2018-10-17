'use strict';
$(document).ready(main);

function main(){

    var registrationError = $('.registration-error-block');
    if(registrationError.length > 0){
        console.log('login error log');
        setTimeout(function(){
            registrationError.slideUp(500);
        }, 5000)
    }

    var emailInput = $('#register-email-input');
    var nameInput = $('#register-name-input');
    var surnameInput = $('#register-surname-input');
    var phoneNumberInput = $('#register-phone-number-input');
    var passwordInput = $('#register-password-input');
    var passwordConfirmationInput = $('#register-password-confirmation-input');
    var submitButton = $('#register-submit');

    emailInput.change(validateEmail);
    nameInput.change(checkNoEmpty.bind(null, nameInput));
    surnameInput.change(checkNoEmpty.bind(null, surnameInput));
    phoneNumberInput.change(validateNumber.bind(null, phoneNumberInput));
    passwordInput.change(checkPasswordStrength.bind(null, passwordInput));
    passwordConfirmationInput.change(
        checkFieldsEqual.bind(null, passwordInput, passwordConfirmationInput));
    submitButton.click(function(event){
        if(!checkSubmitAllowed()){
            event.preventDefault()
        }
    });
}

function resetDefault(item){
    item.removeClass('is-valid');
    item.removeClass('is-invalid');
}

function validateEmailSyntax(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function validateEmail(){
    var emailInput = $(this);
    var email = emailInput.val();
    var incorrectEmailMessage = $('#email-invalid-feedback');

    resetDefault(emailInput);
    incorrectEmailMessage.text('');

    if(!validateEmailSyntax(email)){
        emailInput.addClass('is-invalid');
        incorrectEmailMessage.text('incorrect email syntax');
        return
    }

    function handleResponse(response){
        if(response.existence){
            emailInput.addClass('is-invalid');
            incorrectEmailMessage.text('email already taken');
        }
        else{
            emailInput.addClass('is-valid');
        }
    }

    $.ajax({
        url: '/accounts/ajax_validate_email',
        method: 'GET',
        data: {'email': email},
        datatype: 'json',
        success: handleResponse,
        error: function(response){emailInput.addClass('is-valid')}
    })
}

function checkNoEmpty(inputField){
    resetDefault(inputField);
    var value = inputField.val();
    if(value.length === 0){
        inputField.addClass('is-invalid');
        return
    }
    inputField.addClass('is-valid');
}

function validateNumber(inputField){
    resetDefault(inputField);
    var number = inputField.val();
    function isDigit(c){
        return c >= '0' && c <= '9'
    }
    if(number.length < 7 || number.length > 20 || !number.split().every(isDigit)){
        inputField.addClass('is-invalid');
        return;
    }
    inputField.addClass('is-valid');
}

function checkPasswordStrength(inputField){
    resetDefault(inputField);
    var password = inputField.val();
    if(password.length < 8 || password.length > 32){
        inputField.addClass('is-invalid');
        return;
    }
    inputField.addClass('is-valid');
}

function checkFieldsEqual(primaryField, confirmationField){
    resetDefault(confirmationField);
    if(primaryField.hasClass('is-invalid')) {
        confirmationField.addClass('is-invalid');
        return;
    }
    if(primaryField.val() !== confirmationField.val()){
        confirmationField.addClass('is-invalid');
        return;
    }
    confirmationField.addClass('is-valid');
}

function checkSubmitAllowed(){
    var inputFields = [
        $('#register-email-inpurt'),
        $('#register-name-inpurt'),
        $('#register-surname-inpurt'),
        $('#register-phone-number-inpurt'),
        $('#register-password-inpurt'),
        $('#register-password-confirmation-input')
    ];

    function valid(value){
        return value.hasClass('is-valid')
    }
    return inputFields.every(valid)
}