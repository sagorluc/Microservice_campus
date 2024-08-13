# Standard Library Imports
import datetime
import copy
from decimal import Decimal
from pprint import pprint
import os

# Third-party Library Imports
from zzz_lib.zzz_log import zzz_print, zzz_print_exit
from systemops import for_now_check_order_status

# Django Imports
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView
from resumeweb.models import mcart, mprod_exp180, mcart_fileupload
from resumeweb.views.rw_cart_context import (
    cart_context_forQuerySet, 
    cart_context_forTrackingId, 
    cart_context_loggit
)
from resumeweb.views.vusergroup import test_is_default_group

# Project-Specific Imports
from mymailroom.myfunctions import send_email_customized
from prof_candidate.models import OrderCancellationRequest


TEMPLATE_DIR = "prof_candidate/layout/my_orders/"
APP_VERSION = os.environ.get("VER_RESUMEWEB")

# ******************************************************************************
@user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "MyOrderHistoryView"}))
def MyOrderHistoryView(request):
    zzz_print("    %-28s: %s" % ("MyOrderHistoryView", "********************"))
    template = loader.get_template(TEMPLATE_DIR + "order_history.html")
    
    # qs = mcart.objects.mcartInstance_userOrderHistory(request)
    # zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))
    
    result_ownerid = mcart.objects.mcartInstance_userOrderHistoryByOwnerUniqueId(request)
    # Unpack the tuple into separate variables
    owner_uniqid, cart_instances_ownerid = result_ownerid

    result_owneremail = mcart.objects.mcartInstance_userOrderHistoryByEmailAddress(request)
    # Unpack the tuple into separate variables
    owner_email, cart_instances_owneremail = result_owneremail

    # Now you can use owner_id and cart_instances separately
    # print("Owner ID:", owner_id)
    # print("Cart Instances:", cart_instances)

    context = {
        "no_of_orders":     "result.count()",
        "cart_instances_result_ownerid":   result_ownerid,
        "cart_instances_result_owneremail":     result_owneremail,

        "section_header_1": "My Order History",
        "app_version":      APP_VERSION,
    }
    
    return HttpResponse(template.render(context, request))


# ******************************************************************************
@user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "OrderDetails"}))
def OrderDetailsView(request, tracking_id):
    zzz_print("    %-28s: %s" % ("OrderDetailsView", tracking_id))

    cart_context = cart_context_forTrackingId(request, tracking_id)
    cart_context_loggit(cart_context)

    mcart_instance = cart_context['products_list'][0]['mcart']

    serviceoption_total = 0
    for serviceoption in cart_context['products_list'][0]['mcart_serviceoptions']:
        serviceoption_total += serviceoption.price
    zzz_print("    %-28s: %s" % ("serviceoption_total", serviceoption_total))

    # resume_uploaded = ""
    # if cart_context['resume_required']:
    #     imcart_fileupload = mcart_fileupload.objects.get(
    #         mcompleted_purchase=mcart_instance.mcompleted_purchase
    #     )
    #     resume_uploaded = imcart_fileupload.document

    if mcart_instance:
        # If the mcart instance is found, get the associated mcart_fileupload instance
        mcart_fileupload_instance = mcart_fileupload.objects.filter(
            mcompleted_purchase=mcart_instance.mcompleted_purchase,
            owner_uniqid=mcart_instance.owner_uniqid,
            purchased=True
        ).first()

        if mcart_fileupload_instance:
            # Return the document ID
            resume_document_id = mcart_fileupload_instance.id

    mcart_delivery_total = 0
    if len(cart_context['products_list'][0]['mcart_deliveryoptions']):
        mcart_delivery_total = cart_context['products_list'][0]['mcart_deliveryoptions'][0]
    
    order_cancelation_id = None
    order_cancelation_q = OrderCancellationRequest.objects.filter(created_for=mcart_instance.tracking_id)
    if order_cancelation_q.exists():
        order_cancelation_id = order_cancelation_q.first().submission_conf_id

    ##########################  Check Order Status
    user_email = request.user.email
    order_data = for_now_check_order_status(str(user_email), str(tracking_id))

    order_processing_status = None
    order_is_purchased = None

    m_order = mcart.objects.mcartInstance_userOrderHistory_byTrackingId(request, tracking_id)
    if m_order.exists():
        order_processing_status = m_order.first().processing_status
        order_is_purchased = m_order.first().purchased

    order_status = f"Your order status: {order_processing_status}"
    if order_is_purchased and order_data:
        if order_data[0]["is_reviewed"]:
            order_status = "Your product is being reviewed!"
        elif order_status[0]["is_delivered"]:
            order_status = "Your order is delivered!"
        else:
            order_status = f"Your order status is {order_processing_status}"
    print(f"t_i: {tracking_id}, status:{order_status}")
    ###################################################

    context = {
        "mcart_instance": mcart_instance,
        "cart_context": cart_context,
        "mcart_item_totalcost": cart_context['products_list'][0]['item_totalcost'],
        "mcart_serviceoptions": cart_context['products_list'][0]['mcart_serviceoptions'],
        "mcart_serviceoption_total": serviceoption_total,
        "mcart_deliveryoption": cart_context['products_list'][0]['mcart_deliveryoptions'],
        "mcart_delivery_total": mcart_delivery_total,
        "order_cancelation_id": order_cancelation_id,
        "order_status": order_status,

        "resume_document_id": resume_document_id,
        'section_header_1': "Order Details",
        "app_version": APP_VERSION,
       
    }
    template = loader.get_template(TEMPLATE_DIR + "order_details.html")

    return HttpResponse(template.render(context, request))
