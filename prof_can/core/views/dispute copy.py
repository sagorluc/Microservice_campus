from typing import Any
from guestactions.myfunctions.get_coupon_code import generate_coupon_code
from zzz_lib.zzz_log import zzz_print
import json
from django.db import DataError
from uuid import uuid4
from datetime import datetime
from django.shortcuts import render
from base64 import b64decode, b64encode
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import connection
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from mymailroom.myfunctions import send_email_customized
import datetime
from django.db.models.functions import Substr
import os
from django.views.generic import (
    ListView,
    UpdateView,
    DetailView
)
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

from resumeweb.models import (
    mcart
)
from django.utils import timezone
from ..models import (DisputeSubmissionModel,)
from ..forms import (DisputeSubmissionForm)
from systemops import gen_num_for_email


TEMPLATE_DIR = "prof_candidate/layout/disputes/"
TEMP_DIR_EMAIL = "mymailroom/layout/prof_candidate/"
APP_VERSION = os.environ.get("VER_RESUMEWEB")


# file a dispute
# where customer will be able to submit a dispute aganist an order that is already selected
import datetime
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404, get_object_or_404
# ******************************************************************************
class SubmitDisputeView(LoginRequiredMixin, CreateView):
    template_name   = TEMPLATE_DIR + "submit.html"
    form_class      = DisputeSubmissionForm
    model           = DisputeSubmissionModel
    success_url     = reverse_lazy('prof_candidate:file_disp_with_tracking_id')

    def form_valid(self, form):
        try:
            query = DisputeSubmissionModel.objects.filter(created_aganist__tracking_id=self.kwargs['tracking_id'])
            if query.exists():
                messages.warning(self.request, "A dispute submission already exists for this order")
                return HttpResponseRedirect(self.request.path_info)
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.created_aganist = mcart.objects.get(tracking_id=self.kwargs['tracking_id'])
            self.object.created_at = timezone.now()
            self.object.save()
            user_email_add = self.request.user.email
            subject = "File dispute" + gen_num_for_email()
            # email_body = "You have successfully filed a disputation"   
            time = timezone.now()

            html_message_text = render_to_string(
                template_name=TEMP_DIR_EMAIL + 'file_dispute.html',
                context={"coupon_code_dict": generate_coupon_code()},
                using=None,
                request=None
            )
            plain_message_text = strip_tags(html_message_text)
            appname="SHOPCART"            
            send_email_customized(subject, plain_message_text, html_message_text, user_email_add, appname)

            messages.success(self.request, 'You have successfully submitted your dispute. Please check your email for details.')
            return HttpResponseRedirect(self.request.path_info)
        
        except DataError:
            return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tracking_id'] = self.kwargs['tracking_id']
        context['pg_headline'] = 'File Dispute'
        context['app_version'] = APP_VERSION
        
        return context
        

        
    # def post(self, request, *args, **kwargs):
    #     if request.method == "POST":
    #         form = DisputeForm(request.POST or None)
    #         if form.is_valid():
    #             p = form.save(commit=False)
    #             p.created_by = self.request.user
    #             p.created_at = datetime.datetime.now()
    #             # p.created_aganist = mcart.objects.get(id=self.kwargs['id'])
    #             p.save()
    #             form.save_m2m()
    #             print(self.request.user)
    #             subject = "File dispute"
    #             email_body = "You have successfully disputed a file"    
    #             time = datetime.datetime.now()    
    #             send_email_to_user(self.request.user.email,subject,email_body,time)
    #             return redirect('prof_candidate:dispute_confirm')
    #     else:
    #         form = Dispute()

    # def get_queryset(self):
    #     zzz_print("    %-28s: %s" % ("get_queryset()", ""))
    #     # self.id = get_object_or_404(mcart, id=self.kwargs['id'])
    #     qs = mcart.objects.all()
    #     # qs = mcart.objects.filter(id=self.kwargs['id'])

    #     return qs

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = DisputeForm()
    #     return context






# class SubmitDisputeFromOrderDetails(LoginRequiredMixin, CreateView):
#     template_name = TEMPLATE_DIR + "aganist_order.html"
#     form_class = DisputeForm
#     # model = Dispute
#     # fields = ['dispcause', 'msg']
    

#     # def get_queryset(self):
#     #     zzz_print("    %-28s: %s" % ("get_queryset()", ""))
#     #     # self.id = get_object_or_404(mcart, id=self.kwargs['id'])
#     #     qs = mcart.objects.all()
#     #     # qs = mcart.objects.filter(id=self.kwargs['id'])

#     #     return qs

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = DisputeForm()
    #     context['pgheader'] = "Dispute Against Order"
    #     context['track_id'] = self.kwargs['tracking_id']
    #     context['app_version'] = APP_VERSION
        
    #     return context


#     # def post(self, request, *args, **kwargs):
#     #     if request.method == "POST":
#     #         form = DisputeForm(request.POST or None)
#     #         if form.is_valid():
#     #             p = form.save(commit=False)
#     #             p.created_by = self.request.user
#     #             p.created_at = datetime.datetime.now()
#     #             # p.created_aganist = mcart.objects.get(id=self.kwargs['id'])
#     #             # p.created_aganist = form.cleaned_data['created_aganist']

#     #             p.save()
#     #             form.save_m2m()
#     #             return redirect('prof_candidate:dispute_confirm')
#     #     else:
#     #         form = Dispute()



#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.created_by = self.request.user
#         self.object.created_at = datetime.datetime.now()
#         self.object.created_aganist = self.kwargs['tracking_id']
#         logger.warning(self.object.created_aganist)
#         self.object.save()
#         logger.warning(form)
#         form.save_m2m()
        
        
#         # subject = "File dispute"
#         # email_body = f"You have successfully filled a dispution of {self.tracking id}"   
#         # time = datetime.datetime.now()     
#         # send_email_to_user(self.request.user,subject,email_body,time)

#         return redirect('prof_candidate:dispute_confirm')
#         # return HttpResponse("Form Submitted")




# # ******************************************************************************
# class DisputeConfirmation(LoginRequiredMixin,ListView):
#     model = DisputeClaim
#     template_name = TEMPLATE_DIR + "disp_conf.html"

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(created_by=self.request.user).order_by('-created_at')



# ******************************************************************************
class DisputeResultView(LoginRequiredMixin, ListView):
    model = DisputeSubmissionModel
    template_name = TEMPLATE_DIR + "results.html"

# for decision date sample code
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms


# ******************************************************************************
class DisputeHistoryView(LoginRequiredMixin,ListView):
    model = DisputeSubmissionModel
    template_name = TEMPLATE_DIR + "history.html"

    def get_queryset(self):
        zzz_print("    %-28s: %s" % ("get_queryset()", ""))
        qs = DisputeSubmissionModel.objects.filter(created_by=self.request.user).order_by('created_by').order_by('-created_at')

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        zzz_print("    %-28s: %s" % ("get_context_data()", ""))
        context = super().get_context_data(**kwargs)

        context["no_of_disputes"] = DisputeSubmissionModel.objects.filter(created_by=self.request.user).count()
        context['pgheader'] = "My Dispute History"
        context['app_version'] = APP_VERSION

        for key in context:
            zzz_print("    key %-24s: value %s" % (key, context[key]))

        return context


# ******************************************************************************
class DisputeDetailsView(LoginRequiredMixin, DetailView):
    model = DisputeSubmissionModel
    template_name = TEMPLATE_DIR + "details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['app_version'] = APP_VERSION
        return context
