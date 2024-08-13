import requests
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed, HttpResponseServerError, HttpResponseBadRequest
from inventory.views.shopcart.rw_cart_views import mmh_CartPurchaseSuccess
import uuid
from inventory.models.mcompleted_purchase import mcompleted_purchase
from inventory.models.mcart import mcart
import os
from inventory.models.mamar_pay import mamar_pay
from general.models.buyer_list import BuyerListGuest
from inventory.views.shopcart.rw_cart_context import cart_context_forUser
import logging
from django.conf import settings
logger = logging.getLogger(__name__)
import traceback

global_dict={}

def generate_transaction_id():

    #generate transaction id by uuid module
    transaction_id=uuid.uuid4()

    #generate transaction id by string and random number
    '''character=string.ascii_letters+string.digits
    transaction_id=''.join(random.choice(character) for i in range(20))'''

    #generate transaction id by only random number 
    #transaction_id = f"{int(time.time())}-{random.randint(10000, 99999)}"

    return transaction_id


def initial_payment_amarPay(request):
    # import pdb; pdb.set_trace()
    if request.user.is_authenticated:
        request.session['mmh_guestemailaddress'] = request.user.email
        
        
    global_dict.update(email=request.session['mmh_guestemailaddress'])
    

    tran_id = generate_transaction_id()
    grand_total = cart_context_forUser(request)['total_cost']

    # url = "https://sandbox.aamarpay.com/index.php"
    # payment_base_url = https://sandbox.aamarpay.com
    # payment_base_url = https://secure.aamarpay.com
    # url = os.environ.get('AMAR_PAY_BASE_URL')
    # url = settings.AMAR_PAY_BASE_URL
    # url = "https://sandbox.aamarpay.com/jsonpost.php"
    
    if os.environ.get('SERVER_TYPE') in ["production"]:
        # This is for production
        url = "https://secure.aamarpay.com/index.php"
        payload = {
            "store_id"      : "campuslinker",
            "tran_id"       : tran_id,
            "success_url"   : os.environ.get('AMAR_PAY_SUCCESS_URL'),
            "fail_url"      : os.environ.get('AMAR_PAY_FAIL_URL'),      #"http://www.merchantdomain.com/faile dpage.html",
            "cancel_url"    : "https://campuslinker.com/cart/cart/home/mmh", #os.environ.get('AMAR_PAY_CANCEL_URL'),   #"http://www.merchantdomain.com/can cellpage.html",
            "amount"        : grand_total,
            "currency"      : "BDT",
            "signature_key" : "5d139182a90f1bc7ffcd7cb2056a02cc",
            "desc"          : "CampusLinker Payment",

            "cus_name"      : "CampusLinker guest1",
            "cus_email"     : "arafat.hossain@legoio.com",
            "cus_add1"      : "House B-158 Road 22",
            "cus_add2"      : "Mohakhali DOHS",
            "cus_city"      : "Dhaka",
            "cus_state"     : "Dhaka",
            "cus_postcode"  : "1206",
            "cus_country"   : "Bangladesh",
            "cus_phone"     : "+8801704",
            "type"          : "json"
        }        
    else:
        # This is for non-production
        url = "https://sandbox.aamarpay.com/index.php"
        payload = {
            "store_id"      : "aamarpaytest",
            "tran_id"       : tran_id,
            "success_url"   : os.environ.get('AMAR_PAY_SUCCESS_URL'),
            "fail_url"      : os.environ.get('AMAR_PAY_FAIL_URL'),      #"http://www.merchantdomain.com/faile dpage.html",
            "cancel_url"    : "https://camp2828.dataflightit.com/cart/cart/home/mmh", #os.environ.get('AMAR_PAY_CANCEL_URL'),   #"http://www.merchantdomain.com/can cellpage.html",
            "amount"        : grand_total,
            "currency"      : "BDT",
            "signature_key" : "dbb74894e82415a2f7ff0ec3a97e4183",
            "desc"          : "CampusLinker Payment",

            "cus_name"      : "CampusLinker guest1",
            "cus_email"     : "arafat.hossain@legoio.com",
            "cus_add1"      : "House B-158 Road 22",
            "cus_add2"      : "Mohakhali DOHS",
            "cus_city"      : "Dhaka",
            "cus_state"     : "Dhaka",
            "cus_postcode"  : "1206",
            "cus_country"   : "Bangladesh",
            "cus_phone"     : "+8801704",
            "type"          : "json"
        }

    files=[]
    headers = {}

    # print("Success Url ===================", payload['success_url'])

    # if payload['cancel_url'] is None:
    #     return HttpResponse("cancel_url is None")
    # else:
    #     response = requests.request("POST", url, headers=headers, data=payload, files=files)
    #     print("Payment url------------ " ,response.text)

    #     if data.get('cancel_url') == 'Cancel Url Required. POST cancel_url':
    #         return HttpResponse("cancel_url is None")
    #     else:
    #         data = response.json()
    #     # print("Data ------", data)

    #     return redirect(data['payment_url'])
    #     # return redirect("payment is complete")

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print("Payment url------------ " ,response.text)

    data = response.json()
    # print("Data ------", data)

    return redirect(data['payment_url'])
    # return redirect("payment is complete")


    # pay = aamarPay(isSandbox=True,transactionAmount=63.37)
    # paymentpath = pay.payment()
    # return redirect(paymentpath)
    # Output: paymentpath output https://sandbox.aamarpay.com/paynow.php?track=AAM1636017211119390#

# =============================== Purchase success amarpay =============================
# @csrf_exempt
# def success(request):
#     if request.method == 'POST':
#         payment_data = request.POST
#         converted_payment_data = payment_data.dict()
        
#         # Retrieve transaction ID and total amount
#         transaction_id = payment_data['mer_txnid']
#         total_amount = payment_data['amount']

#         # Retrieve guest email address from global_dict or handle appropriately
#         guest_login_email_address = global_dict.get('email', None)
#         if not guest_login_email_address:
#             # Handle missing guest email address
#             logger.error("Guest email address not found in global_dict")
#             return HttpResponseServerError("Guest email address not found")

#         try:
#             # Save guest email to BuyerListGuest model
#             guest_email = BuyerListGuest.objects.create(
#                 email=guest_login_email_address,
#                 transaction_id=transaction_id
#             )
#             guest_email.save()

#             # Save completed purchase information
#             mcomplete_purchased = mcompleted_purchase(
#                 transaction_id=transaction_id,
#                 total_cost=total_amount,
#                 email_address=guest_login_email_address
#             )
#             mcomplete_purchased.save()

#             # Mark cart items as purchased
#             cart_items = mcart.objects.filter(purchased=False)
#             for item in cart_items:
#                 item.purchased = True
#                 item.save()

#             # Call mmh_CartPurchaseSuccess view to handle purchase completion
#             return mmh_CartPurchaseSuccess(request, transaction_id)

#         except Exception as e:
#             logger.exception(f"Error in success view: {str(e)}")
#             return HttpResponseServerError(f"An error occurred during purchase completion: {str(e)}")
#     else:
#         return HttpResponseBadRequest("Invalid HTTP method")



@csrf_exempt
def success(request):

    if request.method=='POST':

        #email_from_session=request.session['mmh_guestemailaddress']
        #email_from_session="arifulhaque2010@yahoo.com"
        #print("Email from session  ---------------------", email_from_session)
        #getting json data from amar pay
        #convert json data to dictionary and save amar pay model
        payment_data=request.POST
        print("#"*50 ,payment_data, 'line 87')

        convertedPaymentData=payment_data.dict()
        save_payment_data= mamar_pay.objects.create(
            customer_email="global_dict['cus_email']",
            amarpay_payment_data=convertedPaymentData
        )
        save_payment_data.save()

        #Capturing transaction id
        transaction_id=payment_data['mer_txnid']
        total_amount=payment_data['amount']

        # print("#"*50, transaction_id)
        # print("#"*50, total_amount, 'line 101')

        transaction_id=transaction_id


        # Save  guest_email to BuyerListGuest model
        guest_login_email_address= global_dict['email'] # "def274753@gmail.com"
        # print('#'*50, guest_login_email_address, 'line 106')

        guest_email=BuyerListGuest.objects.create(email=guest_login_email_address,transaction_id=transaction_id)
        guest_email.save()

        mcomplete_purchased = mcompleted_purchase(
        transaction_id=transaction_id,
        total_cost=total_amount,
        email_address=guest_login_email_address,
        
        )
        mcomplete_purchased.save()

        cart_items= mcart.objects.filter(purchased=False)
        for items in cart_items:
            items.purchased=True
            items.save()

        return mmh_CartPurchaseSuccess(request,transaction_id)



# https://github.com/aamarpay-dev/aamarPay-python/blob/main/aamarpay/aamarpay.py
# https://aamarpay.readme.io/reference/initiate-payment-json
