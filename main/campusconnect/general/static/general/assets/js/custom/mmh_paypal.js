
// Magic urlPath that point to specific Django Views.
// If the path to the view changes in the python url configuration these need to be changed as well.

const magicUrl_mmh_cartpurchasesuccess  = "/rw/cart/checkout/success/";


// Method duplicated in shopcartmow1.js
// *****************************************************************************
function get_cookie_value(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = get_cookie_value('csrftoken');


// status >>> "Payment Gateway loading failed" 
// *****************************************************************************
function showPaymentGatewayLoadingErrorMsg() {
    let ptst = document.getElementById("payment_gateway_loading_error_msg");
    ptst.removeAttribute("hidden");    
}


// status >>> "Payment Processing successful" 
// *****************************************************************************
function showPaymentProcessingSuccessMsg() {
    let ptst = document.getElementById("successful_payment_processing_status_msg");
    ptst.removeAttribute("hidden");    
}


// status >>> "Payment Processing Failed"
// *****************************************************************************
function showFailedPaymentProcessingStatus() {
    let ptst = document.getElementById("failed_payment_processing_status_msg");
    ptst.removeAttribute("hidden");    
}

