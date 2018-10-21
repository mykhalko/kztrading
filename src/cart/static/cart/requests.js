'use strict';


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function clearItem(item_id){
    console.log(item_id);
    var item = $('#item-row-' + String(item_id));
    item.slideUp(500).remove();
    var purchasesAmountElement = $('#purchases-amount');
    purchasesAmountElement.text(parseInt(purchasesAmountElement.text()) - 1);
    if($('.item-row').length === 0){
        $('.empty-cart-row').slideDown(500);
        $('.non-empty-cart-row').slideUp(500);
        purchasesAmountElement.text('empty')
    }
}

function clearTable(){
    var items = $('.item-row');
    items.slideUp(500).remove();
    var empty_row = $('.empty-cart-row');
    empty_row.slideDown(500);
    var non_empty_row = $('.non-empty-cart-row');
    non_empty_row.slideUp(500);
    $('#purchases-amount').text('empty')
}

function remove(item, url){
    $.ajax({
        url: url,
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        data: {item: item},
        success: clearItem.bind(null, item)
    });
}

function removeAll(url){
    $.ajax({
        url: url,
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        success: clearTable
    });
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

function orderSuccess(item){
    messageUser('Item #' + String(item) + ' ordered successffuly! Thank You!');
    clearItem(item);
}

function ordersSuccess(){
    messageUser('Items ordered successfully! Thank You!');
    clearTable();
}

function order(item, url){
    $.ajax({
        url: url,
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        data: {item: item},
        success: orderSuccess.bind(null, item)
    })
}

function orderAll(url){
    $.ajax({
        url: url,
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        success: ordersSuccess
    })
}
