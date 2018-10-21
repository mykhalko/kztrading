'use strict';

function addToCart(id, url){
    $.ajax({
        method: 'POST',
        url: url,
        data: {
            id: id
        },
        success: additionSuccessActivity
    });
}

function additionSuccessActivity(response){
    if(response.success) {
        purchasesAmountIncrement();
        messageUser('Item added to the cart! Thank You!', 'success');
    }
    else{
        messageUser(response.errors, 'danger')
    }
}

function messageUser(message, alertType){
    var messageBoxHtml =
        '<div id="message-box-id" class="alert alert-' + alertType + ' m-0">' + message + '</div>';
    $('body').prepend(messageBoxHtml);
    var messagebox = $('#message-box-id');
    messagebox.css('border-radius', '0');
    messagebox.hide();
    messagebox.slideDown(500).delay(5000).slideUp(500);
}

function purchasesAmountIncrement() {
    var purchasesAmountElement = $('#purchases-amount');
    var value = parseInt(purchasesAmountElement.text());
    if (isNaN(value)) {
        purchasesAmountElement.text(String(1));
    }
    else {
        value++;
        purchasesAmountElement.text(String(value));
    }
}