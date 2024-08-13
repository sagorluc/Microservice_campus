from zzz_lib.zzz_log import zzz_print, zzz_print_exit

import copy
import json
import random
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

# MMH: What is this????
from django.utils.translation import gettext_lazy as _

from mmhauth.forms import mmhSignInForm

from ...models import mcart_deliveryoptions
from inventory.models.mcart import mcart
from inventory.models.mcart_fileupload import mcart_fileupload
from inventory.models.mcart_serviceoptions import mcart_serviceoptions
from inventory.models.mcompleted_purchase import mcompleted_purchase
from mymailroom.models.msendmail import msendmail
from inventory import const_inventory
from .rw_cart_context import (
    cart_context_forUser,
    cart_context_forMcompletedPurchase,
    highest_priced_product_item_in_cart_context_forUser
)
from general.models import mcoupon_given
from ...models import mcart_coupons 
from general.models.buyer_list import BuyerListGuest
from inventory.models import BuyerInfoModel



from inventory.forms.shopcart.cartCouponForm import  mmhCouponForm
from inventory.forms.shopcart.cartFileUploadForm import  mmhFileUploadForm
from inventory.forms.shopcart.cartGuestLoginForm import  mmhEmailForm


from inventory.validators import validate_email_guest
from mymailroom.myfunctions.send_email import send_email_customized  #send_mail
import logging
logger = logging.getLogger(__name__)
from systemops.my_storage import gen_num_for_email
from guestactions.myfunctions.get_coupon_code import generate_coupon_code
from django.conf import settings





TEMP_DIR_SHOPCART        = 'inventory/shoppingcart/'
TEMP_DIR_SHOPCART_EMAIL  = 'mymailroom/layout/shoppingcart/'



# ******************************************************************************
# @csrf_exempt
def mmh_CartHome_contents(request, mode):
    zzz_print("    %-28s: %s" % ("mmh_CartHome_contents", mode))

    form_errors = []
    if request.method == 'POST':
        # zzz_print("    %-28s: %s" % ("", "request.method == 'POST'"))
        form = mmhCouponForm(data=request.POST)
        # zzz_print("    %-28s: %s" % ("form", form))

        if form.is_valid():
            print(form)
            # zzz_print("    %-28s: %s" % ("", "form.is_valid()"))
            coupon_id = form.cleaned_data.get('coupon_id')
            # zzz_print("    %-28s: %s" % ("coupon_id", coupon_id))

            imcoupon_given = mcoupon_given.objects.check_coupon_exists(request, coupon_id)

            if not imcoupon_given:
                form_errors.append("INVALID COUPON CODE: " + coupon_id)
            else:
                if imcoupon_given.is_coupon_expired():
                    form_errors.append("COUPON EXPIRED: " + coupon_id)
                else:
                    if imcoupon_given.usedinpurchase:
                        form_errors.append("COUPON ALREADY USED: " + coupon_id)
                    else:
                        # TEST IF COUPON IS VALID FOR PRODUCTS IN CART, IE SUBMITTING EXP180 COUPON BUT NO EXP180 PRODUCTS IN CART
                        # Get list of all model_names in cart. Will be used to dtermine if coupon is applicable for cart items.
                        modelname_list_in_cart = []
                        mcart_qs = mcart.objects.mcartQS_usersItemsInCart(request)
                        for mcart_instance in mcart_qs:
                            if mcart_instance.model_name not in modelname_list_in_cart:
                                modelname_list_in_cart.append(mcart_instance.model_name)
                        # for modelname in modelname_list_in_cart:
                        #     zzz_print("    %-28s: %s" % ("modelname", modelname))
                        if imcoupon_given.mcoupon.product_liked not in ['mprod_xyz', 'mprod_adhoc', 'mprod_prei20', 'mprod_intprep', 'mprod_proflevel', 'mprod_posti20', 'mprod_rolebased', 'mprod_strategy', 'mprod_visabased']:
                            form_errors.append("COUPON NOT APPLICABLE FOR ITEMS IN CART: " + coupon_id)
                        else:
                            # --------------------------------- coupon valid apply it.
                            # Determine appropriate mcart instance in cart to apply coupon to
                            imcart = highest_priced_product_item_in_cart_context_forUser(request, imcoupon_given.mcoupon.product_liked)
                            # zzz_print("    %-28s: %s" % ("imcart", imcart))

                            # Delete mcart_coupon_instance this imcoupon_given is previously linked to
                            mcart_coupons.objects.mcart_coupons_delete_any_existing_for_cart_items(request)

                            # create mcart_coupon instance and link it between imcoupon and appropriate mcart instance in cart
                            imcart_coupons = mcart_coupons.objects.mcart_coupons_add_or_update(imcart, imcoupon_given)
                            imcart.refresh_from_db()
                            imcart.save()  # trigger update_final_price
                            # --------------------------------- coupon valid apply it.
        else:
            zzz_print("    %-28s: %s" % ("", "mmhCouponForm is NOT valid()"))
    else:
        # zzz_print("    %-28s: %s" % ("", "request.method != 'POST'"))
        form = mmhCouponForm()

    context = cart_context_forUser(request)

    # DISPLAY CART CONTENTS FOR DEBUGGING
    # from inventory.views.cart_context import cart_context_loggit
    # cart_context_loggit(context)

    # mmh: Hack to trigger display of items for views that use this function.
    #      Other views that use this template won't set this value and so some
    #      items in the template won't display.
    context['mmh_render_for_this_view_only'] = 1
    # context['coupon_form'] = render_to_string(
    #     #TEMP_DIR_SHOPCART+ 'coupon/' +'form.html',
    #     {'form':form, 'form_errors':form_errors},
    #     request=request
    # )

    html = render_to_string(TEMP_DIR_SHOPCART+'components/cart_contents_all.html', context)
    # zzz_print("    %-28s: %s" % ("html", html))

    if   mode == "html":    return html
    elif mode == "ajax":    return JsonResponse({"html":html})
    else:                   return "<b> ERROR: SHOULD NOT GET HERE </b>"


# ******************************************************************************
@csrf_exempt
def rwCartAjaxView_contents(request):
    zzz_print("    %-28s: %s" % ("rwCartAjaxView_contents", ""))
    html = mmh_CartHome_contents(request, "ajax")
    return html


# ******************************************************************************
# @csrf_exempt
def mmh_CartHome_contents_html(request):
    zzz_print("    %-28s: %s" % ("mmh_CartHome_contents_html", ""))
    html = mmh_CartHome_contents(request, "html")
    return html


# ******************************************************************************
def mmh_CartHome(request):
    zzz_print("    %-28s: %s" % ("mmh_CartHome", ""))
    template = loader.get_template(TEMP_DIR_SHOPCART+'base_shopcart.html')
    context = {
        'shopping_cart_contents' : mmh_CartHome_contents_html(request),
        'templatename'           : template.origin.__str__().rsplit('/', 1)[1] if '/' in template.origin.__str__() else '',
        'pg_layout'              : 'carthome',
        'step_num'               : '1',
    }
    return HttpResponse(template.render(context, request))


# ******************************************************************************
def mmh_CartFileUpload(request):
    zzz_print("    %-28s: %s" % ("mmh_CartFileUpload", ""))
    zzz_print("    %-28s: %s" % ("request.method", request.method))
    if request.method == 'POST':
        form = mmhFileUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # import pdb; pdb.set_trace()
            
            document = form.cleaned_data.get('document')
            imcart_fileupload = mcart_fileupload.objects.mcart_fileupload_add_or_update(
                request     = request,
                document    = document,
            )

            print("imcart_fileupload============",imcart_fileupload)

            imcart_fileupload.validate_uploaded_file()

            if imcart_fileupload.validation_passed:
                return HttpResponseRedirect(reverse('mmh_cartcheckout'))
            else:
                request.session['mmh_failed_validation'] = imcart_fileupload.get_validation_method_description(imcart_fileupload.validation_failed_id)
                request.session.modified = True
                return HttpResponseRedirect(reverse('mmh_cartfileupload'))

        else:
            zzz_print("    %-28s: %s" % ("form.is NOT valid()", ""))
            filepath = form.cleaned_data.get('filepath')
            zzz_print("    %-28s: %s" % ("filepath", filepath))
    else:
        form = mmhFileUploadForm()

    # IF THERE WAS A VALIDATION ERROR IN A PREVIOUS UPLOAD GET HTML TO DISPLAY
    file_upload_failure_modal = ""
    if 'mmh_failed_validation' in request.session:
        file_upload_failure_modal = render_to_string(TEMP_DIR_SHOPCART+'components/file_upload/'+'file_uploadfailure_modal_trigger.html', {}, request=request)
        # and remove key from request.session
        # request.session.pop('mmh_failed_validation')
        # request.session.modified = True

    # GET STANDARD CART CONTEXT
    context             = cart_context_forUser(request)
    cart_summary_html   = render_to_string(TEMP_DIR_SHOPCART+'components/summary/sum101.html', context)
    file_upload_form_html = ""
    if context['products_list']:
        file_upload_form_html = render_to_string(TEMP_DIR_SHOPCART+'components/file_upload/'+'form610.html', {'form':form}, request=request)

    template = loader.get_template(TEMP_DIR_SHOPCART+'components/file_upload/file_upload.html')
    context = {
        'file_upload_form_html'         : file_upload_form_html,
        'file_upload_failure_msg'       : file_upload_failure_modal,
        'file_upload_general_rules'     : True,
        'cart_summary_html'             : cart_summary_html,
        'templatename'                  : template.origin.__str__().rsplit('/', 1)[1] if '/' in template.origin.__str__() else '',
        'pg_layout'                     : 'cartfileupload',
        'step_num'                      : '2',
    }
    return HttpResponse(template.render(context, request))


# ******************************************************************************
def mmh_CartUserLogin(request):
    zzz_print("    %-28s: %s" % ("mmh_CartUserLogin", ""))

    if request.user.is_authenticated:
        zzz_print("    %-28s: %s" % ("", "request.user.is_authenticated"))
        return {'redirect': '/cart/checkout/sign-in/mmh/loginorguestsuccess'}

    if request.method == 'GET':
        zzz_print("    %-28s: %s" % ("", "request.method == 'GET'"))
        form = mmhSignInForm()
        return {'html': render_to_string(TEMP_DIR_SHOPCART+ 'components/userlogin/' +'form_reguser.html', {'form': form}, request)}

    if request.method == 'POST':
        zzz_print("    %-28s: %s" % ("", "request.method == 'POST'"))
        form = mmhSignInForm(data=request.POST)
        if form.is_valid():
            zzz_print("    %-28s: %s" % ("", "form.is_valid()"))
            email    = form.cleaned_data.get("email").lower()
            password = form.cleaned_data.get("password")
            # zzz_print("    %-28s: %s" % ("email", email))
            # zzz_print("    %-28s: %s" % ("password", password))
            # 2021/05/25: Users now log in with their email address.
            #             But we are still using Django's default user model.
            #             We no longer ask for a username when creating a new account.
            #             Instead we force a lower case version of the users email address into their username.
            #             And we use this email address as their username.
            user = authenticate(username=email, password=password)
            if user is not None:
                zzz_print("    %-28s: %s" % ("", "user is not None"))
                login(request, user)
                return {'redirect': '/cart/checkout/sign-in/mmh/loginorguestsuccess'}
            else:
                zzz_print("    %-28s: %s" % ("", "user IS None"))
                form_errors = "Invalid Email Address or Password"
                zzz_print("    %-28s: %s" % ("user did not authenticate", ""))
                zzz_print("    %-28s: %s" % ("email", email))
                zzz_print("    %-28s: %s" % ("password", password))
                return {'html': render_to_string(TEMP_DIR_SHOPCART+'components/userlogin/' +'form_reguser.html', {'form': form, "form_errors": form_errors}, request)}
        else:
            zzz_print("    %-28s: %s" % ("", "form.is NOT valid()"))
            return {'html': render_to_string(TEMP_DIR_SHOPCART+'components/userlogin/' +'form_reguser.html', {'form': form}, request)}


# ******************************************************************************
def mmh_CartGuestLogin(request):
    zzz_print("    %-28s: %s" % ("mmh_CartGuestLogin", ""))

    if request.user.is_authenticated:
        zzz_print("    %-28s: %s" % ("", "request.user.is_authenticated"))
        return {'redirect': '/cart/checkout/sign-in/mmh/loginorguestsuccess'}

    if request.method == 'GET':
        zzz_print("    %-28s: %s" % ("", "request.method == 'GET'"))
        form = mmhEmailForm()
        context = {
            'html': render_to_string(
                    TEMP_DIR_SHOPCART+ 'components/' + 'userlogin/' +'form_guest.html', 
                    {'form': form}, 
                    request = request
                )
        }
        return context

    if request.method == 'POST':
        zzz_print("    %-28s: %s" % ("", "request.method == 'POST'"))
        form = mmhEmailForm(data=request.POST)
        if form.is_valid():
            zzz_print("    %-28s: %s" % ("", "form.is_valid()"))
            guest_email_given = form.cleaned_data.get('email')
            request.session['mmh_guestemailaddress'] = guest_email_given
            request.session.modified = True
            return HttpResponseRedirect('/cart/checkout/sign-in/mmh/loginorguestsuccess')
        else:
            zzz_print("    %-28s: %s" % ("", "form.is NOT valid()"))
            return {'html': render_to_string(TEMP_DIR_SHOPCART+'guest_email_form.html', {'form': form}, request)}


# ******************************************************************************
def mmh_CartLoginPage(request):
    zzz_print("    %-28s: %s" % ("mmh_CartLoginPage", ""))
    template = loader.get_template(TEMP_DIR_SHOPCART+'layout/'+'user_login.html')

    user_login_html         = "user_login_html_NOT_POPULATED"
    proceed_as_guest_html   = "proceed_as_guest_html_NOT_POPULATED"
    cart_summary_html       = "cart_summary_html_NOT_POPULATED"

    # # hack to delete session cookie
    # zzz_print("    %-28s: %s" % ("HACK TO DELETE mmh_guestemailaddress", "IS ENABLED"))
    # zzz_print("    %-28s: %s" % ("HACK TO DELETE mmh_guestemailaddress", "IS ENABLED"))
    # # if 'mmh_guestemailaddress' in request.session:
    # #     del request.session['mmh_guestemailaddress']
    # zzz_print("    %-28s: %s" % ("HACK TO DELETE mmh_guestemailaddress", "IS ENABLED"))
    # zzz_print("    %-28s: %s" % ("HACK TO DELETE mmh_guestemailaddress", "IS ENABLED"))

    # if not request.user.is_authenticated and 'mmh_guestemailaddress' not in request.session:
    if not request.user.is_authenticated:
        zzz_print("    %-28s: %s" % ("mmh_CartLoginPage", "user IS NOT authenticated"))

        return_dict = mmh_CartUserLogin(request)
        if   'html' in return_dict:         user_login_html = return_dict['html']
        elif 'redirect' in return_dict:     return redirect(return_dict['redirect'])
        else:                               zzz_print("    %-28s: %s" % ("WARNING mmh_CartLoginPage", "neither html nor redirect found in return_dict"))

        return_dict = mmh_CartGuestLogin(request)
        if   'html' in return_dict:         proceed_as_guest_html = return_dict['html']
        elif 'redirect' in return_dict:     return redirect(return_dict['redirect'])
        else:                               zzz_print("    %-28s: %s" % ("WARNING mmh_CartLoginPage", "neither html nor redirect found in return_dict"))

        context             = cart_context_forUser(request)
        cart_summary_html   = render_to_string(TEMP_DIR_SHOPCART+'components/summary/sum101.html', context)
    else:
        zzz_print("    %-28s: %s" % ("mmh_CartLoginPage", "user IS authenticated OR guest"))
        return HttpResponseRedirect('/cart/checkout/sign-in/mmh/loginorguestsuccess')

    context = {
        'user_login_html'       : user_login_html,
        'proceed_as_guest_html' : proceed_as_guest_html,
        'cart_summary_html'     : cart_summary_html,
        'templatename'          : template.origin.__str__().rsplit('/', 1)[1] if '/' in template.origin.__str__() else '',
        'pg_layout'             : 'cartlogin',
        'step_num'              : '3',
    }
    return HttpResponse(template.render(context, request))


import os
# ******************************************************************************
def mmh_CartLoginOrGuestSuccess(request):
    zzz_print("    %-28s: %s" % ("mmh_CartLoginOrGuestSuccess", ""))
    template = loader.get_template(TEMP_DIR_SHOPCART+'layout/'+'amarpay_checkout.html')

    context                         = cart_context_forUser(request)
    cart_summary_html               = render_to_string(TEMP_DIR_SHOPCART+'components/summary/' +'sum101.html', context)
    payment_buttons_container_html   = render_to_string(TEMP_DIR_SHOPCART+'components/checkout/'+'payment_buttons_container.html', {})

    context = {
        'payment_buttons_container_html'   : payment_buttons_container_html,
        'cart_summary_html'               : cart_summary_html,
        'templatename'                    : template.origin.__str__().rsplit('/', 1)[1] if '/' in template.origin.__str__() else '',
        'my_client_id'                    : os.environ.get('PAYMENT_CLIENT_ID'),
        'pg_layout'                       : 'cartlogin',
        'step_num'                        : '4',
    }
    return HttpResponse(template.render(context, request))


def mmh_CartPurchaseSuccess(request, transaction_id):
    zzz_print("    %-28s: %s" % ("mmh_CartPurchaseSuccess", ""))
    zzz_print("    %-28s: %s" % ("transaction_id", transaction_id))
    template = loader.get_template(TEMP_DIR_SHOPCART+'layout/'+'purchase_conf.html')
    user_email_receiving_purchase_confirmation = ""
    logger.warning("cart purchase success view")
    imcompleted_purchase = mcompleted_purchase.objects.get(transaction_id=transaction_id)
    # print('#'*20, imcompleted_purchase, 'line 392')
    user_email_add = imcompleted_purchase.email_address
    # cus_email = request.POST.get('cus_email')
    # total_cost = request.POST.get('amount')
    # print('#'*50, user_email_add,'line 394')
    # print('#'*50, cus_email, 'line 395')
    # print('#'*50, total_cost, 'line 398')
    # print('#'*50, request.POST, 'line 397')

    
    if request.user.is_authenticated:
        # print('#'*40,'Line 399')
        logger.warning("cart purchase success user is auth or not check")
        user_email_receiving_purchase_confirmation = user_email_add = request.user.email

        # save buyer information in BuyerInfoModel table
        buyer_info                   = BuyerInfoModel()
        buyer_info.purchase_id       = imcompleted_purchase.id
        buyer_info.email_address     = request.user.email
        buyer_info.buyer_type        = "r"
        buyer_info.save()
        

    elif 'mmh_guestemailaddress' in request.session:
        print('#'*40,'Line 412')
        imcompleted_purchase.save()
        logger.warning(f"cart purchased successfully guest users email address: {request.session['mmh_guestemailaddress']}")
        user_email_receiving_purchase_confirmation = user_email_add = request.session['mmh_guestemailaddress']

        # save buyer information in BuyerInfoModel table
        buyer_info                   = BuyerInfoModel()
        buyer_info.purchase_id       = imcompleted_purchase.id
        buyer_info.email_address     = request.session['mmh_guestemailaddress']
        buyer_info.buyer_type        = "g"
        buyer_info.save()

    else:
        print('#'*40,'Line 431')
        zzz_print("    %-28s: %s" % ("WARNING", "(NOT request.user.is_authenticated) AND (mmh_guestemailaddress NOT in request.session)"))
        user_email_receiving_purchase_confirmation = imcompleted_purchase.email_address

    # Email templete
    cart_context = cart_context_forMcompletedPurchase(request, imcompleted_purchase)
    cart_context["imcompleted_purchase"]   = imcompleted_purchase
    cart_context["delivery_email_address"] = user_email_receiving_purchase_confirmation    
    cart_context["coupon_code_dict"] = generate_coupon_code()

    # send email to the user
    appname = "SHOPCART"
    subject = "CampusLinker purchase confirmation # " + str(imcompleted_purchase.transaction_id)[0:8] + "-" + gen_num_for_email()
    html_message_text = render_to_string(
        template_name=TEMP_DIR_SHOPCART_EMAIL + 'shopcart_main.html',
        context=cart_context,
        using=None,
        request=None
    )
    plain_message_text = strip_tags(html_message_text)
    send_email_customized(subject, plain_message_text, html_message_text, user_email_add, appname)
    
    context = {
        'mcompletedpurchase_id'     : imcompleted_purchase.id,
        'transaction_id'            : imcompleted_purchase.transaction_id,
        'email_address_list'        : user_email_add, # cus_email # list(dict.fromkeys(user_email_add)), # Remove duplicates from to_emails_list
        'electronic_delivery_email' : user_email_receiving_purchase_confirmation,
        'date_time'                 : imcompleted_purchase.created,
        'shopping_cart_contents'    : render_to_string(TEMP_DIR_SHOPCART+'components/'+'cart_contents_all.html', cart_context),
        'templatename'              : template.origin.__str__().rsplit('/', 1)[1] if '/' in template.origin.__str__() else '',
        'app_version'               : settings.APP_VERSION,
    }
    logger.warning(f"purchase information view passing context: {context}")
    return HttpResponse(template.render(context, request))


# ******************************************************************************
@csrf_exempt
def rwCartAjaxView_carticon(request):
    # zzz_print("    %-28s: %s" % ("rwCartAjaxView_carticon", ""))
    qs = mcart.objects.mcartQS_usersItemsInCart(request)
    context = {
        'cart_item_count' : qs.count(),
    }
    html = render_to_string('general/components/menus/header/cart_button_02072022.html', context)
    # zzz_print("    %-28s: %s" % ("html", html))
    return JsonResponse({"html":html})


# ******************************************************************************
@csrf_exempt
def rwCartAjaxView_emptycart(request):
    zzz_print("    %-28s: %s" % ("rwCartAjaxView_emptycart", "START: ***************************"))
    if request.method == "POST":
        qs = mcart.objects.mcartQS_usersItemsInCart(request)
        zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))
        for item in qs:
            # mmh: 2021_08_04
            # item.set_removed()
            mcart.objects.remove_ver2(
                request                     = request,
                item_id                     = item.item_id,
                model_name                  = item.model_name,
            )

        zzz_print("    %-28s: %s" % ("rwCartAjaxView_emptycart", "END: ***************************"))
        return JsonResponse({"response":'success'})
    elif request.method == "GET":
        zzz_print("    %-28s: %s" % ("rwCartAjaxView_emptycart", "request.method == GET"))
        zzz_print("    %-28s: %s" % ("rwCartAjaxView_emptycart", "raise Http404(Not found)"))
        raise Http404("Not found")


# ******************************************************************************
@csrf_exempt
def rwCartAjaxView_removebymodelnameandid(request):
    zzz_print("    %-28s: %s" % ("rwCartAjaxView_removebymodelnameandid", "START: ***************************"))
    if request.method == "POST":
        model_name      = request.POST.get("model_name")
        item_id         = request.POST.get("id")
        zzz_print("    %-28s: %s" % ("model_name", model_name))
        zzz_print("    %-28s: %s" % ("item_id", item_id))

        qs = mcart.objects.mcartQS_modelNameAndIdItemsInCart(request, model_name, item_id)
        if qs.count() != 1:
            zzz_print("    %-28s: %s %s" % ("WARNING # QUESTION: .count()", "rwCartAjaxView_removebymodelnameandid", qs.count()))
        for item in qs:
            # mmh: 2021_08_04
            # item.set_removed()
            mcart.objects.remove_ver2(
                request                     = request,
                item_id                     = item.item_id,
                model_name                  = item.model_name,
            )

        zzz_print("    %-28s: %s" % ("rwCartAjaxView_removebymodelnameandid", "END: ***************************"))
        return JsonResponse({"response":'success'})
    elif request.method == "GET":
        zzz_print("    %-28s: %s" % ("rwCartAjaxView_removebymodelnameandid", "request.method == GET"))
        zzz_print("    %-28s: %s" % ("rwCartAjaxView_removebymodelnameandid", "raise Http404(Not found)"))
        raise Http404("Not found")


# ******************************************************************************
def does_product_model_name_require_resume_file_upload(model_name):
    zzz_print("    %-28s: %s" % ("does_product_model_name_require_resume_file_upload", model_name))

    if model_name in const_inventory.MODELNAME_BOOLEAN_DICT_PRODUCTS_THAT_WORK_IN_CART_SYSTEM_RESUME_REQUIRED:
        zzz_print("    %-28s: %s" % ("model_name FOUND in dict", model_name))
        return const_inventory.MODELNAME_BOOLEAN_DICT_PRODUCTS_THAT_WORK_IN_CART_SYSTEM_RESUME_REQUIRED[model_name]
    else:
        zzz_print_exit("    %-28s: %s" % ("model_name NOT FOUND in dict", model_name))
        return False # but it will not get here as above logx statement will raise exception


# ******************************************************************************
@csrf_exempt
def rwCartAjaxView_addproductver2(request):
    zzz_print("    %-28s: %s" % ("rwCartAjaxView_addproductver2", "START: ***************************"))
    if request.method == "POST":
        product_ver2 = request.POST.getlist("product_ver2[]")
        product_ver2 = json.loads(product_ver2[0])

        checked_service_option_id_list  = product_ver2["serviceoptions"]
        checked_delivery_option_id_list = product_ver2["deliveryoption"]
        # for id in checked_service_option_id_list:
        #     zzz_print("    %-28s: %s" % ("checked service option id", id))
        # for id in checked_delivery_option_id_list:
        #     zzz_print("    %-28s: %s" % ("checked delivery option id", id))

        resume_required = does_product_model_name_require_resume_file_upload(product_ver2["model_name"])
        # zzz_print("    %-28s: %s" % ("resume_required", resume_required))

        mcart.objects.mcart_add_or_update_ver2(
            request                     = request,
            item_id                     = product_ver2["id"],
            model_name                  = product_ver2["model_name"],
            quantity                    = product_ver2["quantity"],
            service_option_id_list      = product_ver2["serviceoptions"],
            delivery_option_id_list     = product_ver2["deliveryoption"],
            resume_required             = resume_required,
        )

        zzz_print("    %-28s: %s" % ("rwCartAjaxView_addproductver2", "END: ***************************"))
        return JsonResponse({"response":'success'})
    elif request.method == "GET":
        zzz_print("    %-28s: %s" % ("rwCartAjaxView_addproductver2", "request.method == GET"))
        zzz_print("    %-28s: %s" % ("rwCartAjaxView_addproductver2", "raise Http404(Not found)"))
        raise Http404("Not found")


# ******************************************************************************
@csrf_exempt
def rwCartAjaxView_removeproductver2(request):
    zzz_print("    %-28s: %s" % ("rwCartAjaxView_removeproductver2", "START: ***************************"))
    if request.method == "POST":
        product_ver2 = request.POST.getlist("product_ver2[]")
        product_ver2 = json.loads(product_ver2[0])
        # zzz_print("    %-28s: %s" % ("len(product_ver2)",         len(product_ver2)))
        # zzz_print("    %-28s: %s" % ("product_ver2[id]",          product_ver2["id"]))
        # zzz_print("    %-28s: %s" % ("product_ver2[model_name]",  product_ver2["model_name"]))
        # zzz_print("    %-28s: %s" % ("product_ver2[quantity]",    product_ver2["quantity"]))

        # checked_service_option_id_list  = product_ver2["serviceoptions"]
        # checked_delivery_option_id_list = product_ver2["deliveryoption"]
        # for id in checked_service_option_id_list:
        #     zzz_print("    %-28s: %s" % ("checked service option id", id))
        # for id in checked_delivery_option_id_list:
        #     zzz_print("    %-28s: %s" % ("checked delivery option id", id))

        mcart.objects.remove_ver2(
            request                     = request,
            item_id                     = product_ver2["id"],
            model_name                  = product_ver2["model_name"],
        )

        zzz_print("    %-28s: %s" % ("rwCartAjaxView_removeproductver2", "END: ***************************"))
        return JsonResponse({"response":'success'})
    elif request.method == "GET":
        zzz_print("    %-28s: %s" % ("rwCartAjaxView_removeproductver2", "request.method == GET"))
        zzz_print("    %-28s: %s" % ("rwCartAjaxView_removeproductver2", "raise Http404(Not found)"))
        raise Http404("Not found")



# # ******************************************************************************
# @csrf_exempt
# def rwCartAjaxView_unapplycoupontocart(request, string32):
#     zzz_print("    %-28s: %s" % ("rwCartAjaxView_unapplycoupontocart", "START: ***************************"))
#     zzz_print("    %-28s: %s" % ("string32", string32))
#     if request.method == "POST":
#         imcoupon_given = mcoupon_given.objects.get_valid_mcoupon_given_for_user(request, string32)
#         zzz_print("    %-28s: %s" % ("imcoupon_given", imcoupon_given))
#
#         # Delete mcart_coupon_instance this imcoupon_given is linked to
#         imcart_coupons = imcoupon_given.mcart_coupons
#         # zzz_print("    %-28s: %s" % ("imcart_coupons", imcart_coupons))
#         imcart = imcart_coupons.mcart
#         zzz_print("    %-28s: %s" % ("imcart", imcart))
#         imcart_coupons.delete()
#         zzz_print("    %-28s: %s" % ("DELETED imcart_coupons", "DELETED imcart_coupons"))
#         imcart.refresh_from_db() # To refresh instance because we just deleted a one to one relationship
#         imcart.save()  # trigger update_final_price
#
#
#
#         zzz_print("    %-28s: %s" % ("rwCartAjaxView_unapplycoupontocart", "END: ***************************"))
#         return JsonResponse({"response":'success'})
#     elif request.method == "GET":
#         zzz_print("    %-28s: %s" % ("rwCartAjaxView_unapplycoupontocart", "request.method == GET"))
#         zzz_print("    %-28s: %s" % ("rwCartAjaxView_unapplycoupontocart", "raise Http404(Not found)"))
#         raise Http404("Not found")
#
# # ******************************************************************************
# @csrf_exempt
# def rwCartAjaxView_applycoupontocart(request, string32):
#     zzz_print("    %-28s: %s" % ("rwCartAjaxView_applycoupontocart", "START: ***************************"))
#     zzz_print("    %-28s: %s" % ("string32", string32))
#     if request.method == "POST":
#         imcoupon_given = mcoupon_given.objects.get_valid_mcoupon_given_for_user(request, string32)
#         zzz_print("    %-28s: %s" % ("imcoupon_given", imcoupon_given))
#
#         # Determine appropriate mcart instance in cart ????
#         imcart = highest_priced_product_item_in_cart_context_forUser(request, imcoupon_given.mcoupon.category)
#
#         # create mcart_coupon instance and link it between
#         # imcoupon and appropriate mcart instance in cart
#         imcart_coupons = mcart_coupons.objects.mcart_coupons_add_or_update(imcart, imcoupon_given)
#         imcart.save()  # trigger update_final_price
#
#
#
#         zzz_print("    %-28s: %s" % ("rwCartAjaxView_applycoupontocart", "END: ***************************"))
#         return JsonResponse({"response":'success'})
#     elif request.method == "GET":
#         zzz_print("    %-28s: %s" % ("rwCartAjaxView_applycoupontocart", "request.method == GET"))
#         zzz_print("    %-28s: %s" % ("rwCartAjaxView_applycoupontocart", "raise Http404(Not found)"))
#         raise Http404("Not found")

# # ******************************************************************************
# @csrf_exempt
# def rwCartAjaxView_applycoupon(request):
#     zzz_print("    %-28s: %s" % ("rwCartAjaxView_applycoupon", "**************************"))
#     zzz_print("    %-28s: %s" % ("rwCartAjaxView_applycoupon", "**************************"))
#     zzz_print("    %-28s: %s" % ("rwCartAjaxView_applycoupon", "**************************"))
#     zzz_print("    %-28s: %s" % ("rwCartAjaxView_applycoupon", "**************************"))
#
#     if request.method == 'POST':
#         zzz_print("    %-28s: %s" % ("", "request.method == 'POST'"))
#         form = mmhCouponForm(data=request.POST)
#         zzz_print("    %-28s: %s" % ("form", form))
#         if form.is_valid():
#             zzz_print("    %-28s: %s" % ("", "form.is_valid()"))
#             coupon_id = form.cleaned_data.get('coupon_id')
#             zzz_print("    %-28s: %s" % ("coupon_id", coupon_id))
#
# 			# return JsonResponse({"response":'success'})
#             return HttpResponse('')
#         else:
#             zzz_print("    %-28s: %s" % ("", "form.is NOT valid()"))
#
# 			# return {'html': render_to_string(TEMP_DIR_SHOPCART+'tguestemailform.html', {'form': form}, request)}
#             return HttpResponse('')
#     else:
#         zzz_print("    %-28s: %s" % ("", "request.method != 'POST'"))
#
# 		# form = mmhCouponForm()
# 		# return JsonResponse({"response":'success'})
#         return HttpResponse('')

