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

# Standard Library Imports
import datetime
import copy
from decimal import Decimal
from pprint import pprint
import os

# Project-Specific Imports
from core.models import OrderCancellationRequest
from ..my_func import (
    get_users_purchase_history, 
    get_purchased_order_data,
    calculate_grace_period,
    
)


TEMPLATE_DIR = "prof_candidate/layout/my_orders/"
APP_VERSION = os.environ.get("VER_RESUMEWEB")

from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone

# views.py (in the second microservice)
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import AnonymousUser

class MyOrderHistoryApiView(APIView):
    def get(self, request):
        email = request.query_params.get('email', None)
        if not email:
            return Response({"detail": "Email address is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch BuyerInfo data
        buyerinfo_url = 'http://127.0.0.1:8000/buyerinfo_mcart/api/buyerinfo/'
        buyerinfo_response = requests.get(buyerinfo_url, params={'email_address': email})
        if buyerinfo_response.status_code != 200:
            return Response({"error": "Failed to fetch buyer info"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        buyerinfo_data = buyerinfo_response.json()

        # Extract purchase IDs
        pur_email = [item['email_address'] for item in buyerinfo_data]

        # Fetch mcart data
        mcart_url = 'http://127.0.0.1:8000/buyerinfo_mcart/api/mcart/'
        mcart_response = requests.get(mcart_url, params={'email_address': pur_email})
        if mcart_response.status_code != 200:
            return Response({"error": "Failed to fetch cart items"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        mcart_data = mcart_response.json()

        return Response({
            "buyerinfo": buyerinfo_data,
            # "mcart": mcart_data
        }, status=status.HTTP_200_OK)
        
        

# class MyOrderHistoryApiView(APIView):
#     def get(self, request):
#         if isinstance(request.user, AnonymousUser):
#             return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

#         email = request.user.email

#         # Fetch BuyerInfo data
#         buyerinfo_url = 'http://127.0.0.1:8000/buyerinfo_mcart/api/buyerinfo/'
#         buyerinfo_response = requests.get(buyerinfo_url, params={'email_address': email})
#         if buyerinfo_response.status_code != 200:
#             return Response({"error": "Failed to fetch buyer info"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         buyerinfo_data = buyerinfo_response.json()

#         # Extract purchase IDs
#         purchase_ids = [item['purchase_id'] for item in buyerinfo_data]

#         # Fetch mcart data
#         mcart_url = 'http://127.0.0.1:8000/buyerinfo_mcart/api/mcart/'
#         mcart_response = requests.get(mcart_url, params={'purchase_ids': purchase_ids})
#         if mcart_response.status_code != 200:
#             return Response({"error": "Failed to fetch cart items"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         mcart_data = mcart_response.json()

#         return Response({
#             "buyerinfo": buyerinfo_data,
#             "mcart": mcart_data
#         }, status=status.HTTP_200_OK)

    

# ******************************************************************************
def MyOrderHistoryView(request):
    # import pdb; pdb.set_trace()
    template = loader.get_template(TEMPLATE_DIR + "order_history.html")

    ## Get tracking_id_list raw data for a given user
    tracking_id_list_queryset = get_users_purchase_history(request.user.email)
    # print("tracking_id_list_queryset >>{}".format(tracking_id_list_queryset))

    ## Get tracking id list from  tracking_id_list_queryset
    tracking_id_list = [item for sublist in tracking_id_list_queryset for item in sublist]
    tracking_ids = [item.tracking_id for item in tracking_id_list]
    # print("tracking_ids {}".format(tracking_ids))
    # print("len tracking_ids {}".format(len(tracking_ids)))

    if len(tracking_ids) == 0:
        server_msg = "You do not have any order yet"

        context = {
            "no_of_transactions"        : len(tracking_id_list_queryset),
            "no_of_orders"              : len(tracking_ids),
            "user"                      : request.user,
            "server_msg"                : server_msg,

            "section_header_1"          : "My Order History",
            "app_version"               : APP_VERSION,
        }

    else:
        purshased_order_list = get_purchased_order_data(tracking_ids, request)
        # print("purshased_order_list >>{}".format(purshased_order_list))
        purshased_order_list_sorted = sorted(purshased_order_list, key=lambda x: x['created'][0], reverse=True)

        check_grace_period = calculate_grace_period(purshased_order_list_sorted)

        context = {
            "no_of_transactions"        : len(tracking_id_list_queryset),
            "no_of_orders"              : len(tracking_ids),
            "user"                      : request.user,
            "tracking_id_list"          : tracking_id_list_queryset,
            "purshased_order_list"      : purshased_order_list_sorted,
            "grace_period"              : check_grace_period,

            "section_header_1"          : "My Order History",
            "app_version"               : APP_VERSION,
        }
    
    return HttpResponse(template.render(context, request))


# ******************************************************************************
def OrderDetailsView(request, tracking_id):
    cart_context = cart_context_forTrackingId(request, tracking_id)
    cart_context_loggit(cart_context)
    mcart_instance = cart_context['products_list'][0]['mcart']

    # Get associated mcart_fileupload instance
    if mcart_instance:
        mcart_fileupload_instance = mcart_fileupload.objects.filter(
            mcompleted_purchase=mcart_instance.mcompleted_purchase,
            owner_uniqid=mcart_instance.owner_uniqid,
            purchased=True
        ).first()

        if mcart_fileupload_instance:
            # Return the document ID
            resume_document_id = mcart_fileupload_instance.id

    resume_uploaded = ""
    if cart_context['resume_required']:
        imcart_fileupload = mcart_fileupload.objects.get(
            mcompleted_purchase=mcart_instance.mcompleted_purchase
        )
        resume_uploaded = imcart_fileupload.document

    # Get pricing data >> service option
    serviceoption_total = 0
    for serviceoption in cart_context['products_list'][0]['mcart_serviceoptions']:
        serviceoption_total += serviceoption.price
    zzz_print("    %-28s: %s" % ("serviceoption_total", serviceoption_total))

    # Get pricing data >> delivery option
    mcart_delivery_total = 0
    if len(cart_context['products_list'][0]['mcart_deliveryoptions']):
        mcart_delivery_total = cart_context['products_list'][0]['mcart_deliveryoptions'][0]
    
    order_cancelation_id = None
    order_cancelation_q = OrderCancellationRequest.objects.filter(created_for=mcart_instance.tracking_id)
    if order_cancelation_q.exists():
        order_cancelation_id = order_cancelation_q.first().submission_conf_id

    ######## Check Order Status
    user_email = request.user.email
    order_progress_status = check_order_progress_status(str(user_email), str(tracking_id))
    # print(f"order_progress_status: {order_progress_status}")
    if order_progress_status:
        order_progress_status = int(order_progress_status[0]["order_progress"])
    else: 
        order_progress_status = 5
    ########

    context = {
        "mcart_instance": mcart_instance,
        "cart_context": cart_context,
        "mcart_item_totalcost": cart_context['products_list'][0]['item_totalcost'],
        "mcart_serviceoptions": cart_context['products_list'][0]['mcart_serviceoptions'],
        "mcart_serviceoption_total": serviceoption_total,
        "mcart_deliveryoption": cart_context['products_list'][0]['mcart_deliveryoptions'],
        "mcart_delivery_total": mcart_delivery_total,
        "order_cancelation_id": order_cancelation_id,
        "order_status": order_progress_status,

        "resume_document_id": resume_document_id,
        "resume_uploaded": resume_uploaded,
        
        'section_header_1': "Order Details",
        "app_version": APP_VERSION,
       
    }
    template = loader.get_template(TEMPLATE_DIR + "order_details.html")

    return HttpResponse(template.render(context, request))
