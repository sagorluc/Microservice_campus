from typing import Any
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

from django.utils import timezone
from ..models import (DisputeSubmissionModel,)
from ..forms import (DisputeSubmissionForm)


TEMPLATE_DIR    = "prof_candidate/layout/disputes/"
TEMP_DIR_EMAIL  = "mymailroom/layout/prof_candidate/"
# APP_VERSION     = settings.VER_RESUMEWEB


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
    success_msg     = 'You have successfully submitted a dispute. '
    success_msg    += 'Please check your email for details.'

    def form_valid(self, form):
        try:
            query = DisputeSubmissionModel.objects.filter(created_aganist__tracking_id=self.kwargs['tracking_id'])
            if query.exists():
                messages.warning(self.request, "A dispute has already been submitted for this order")
                return HttpResponseRedirect(self.request.path_info)
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.created_aganist = mcart.objects.get(tracking_id=self.kwargs['tracking_id'])
            self.object.created_at = timezone.now()
            self.object.save()

            # generate/select a coupon code from coupon table
            cop_code_dict   = generate_coupon_code()

            # send email to the user
            appname         = "CUSTSUPP"
            subject         = "CampusLinker Dispute Confirmation # " + gen_num_for_email()
            user_email_add  = self.request.user.email
            
            email_context   = {
                'submission_id'     : str(uuid4())[:6],
                'submission_time'   : datetime.datetime.now(),
                'coupon_code_dict'  : cop_code_dict,
            }
            html_message_text = render_to_string(
                template_name=TEMP_DIR_EMAIL + 'file_dispute.html',
                context=email_context,
                using=None,
                request=None
            )
            plain_message_text = strip_tags(html_message_text)
            send_email_customized(subject, plain_message_text, html_message_text, user_email_add, appname)
            # email function ends

            messages.success(self.request, self.success_msg)
            return super().form_valid(form)
    
        except DataError:
            return super().form_valid(form)

    def get_success_url(self):
        # import pdb; pdb.set_trace()
        # tracking_id = self.request.get('tracking_id')
        tracking_id = self.kwargs['tracking_id']
        # success_url = reverse_lazy('prof_candidate:file_disp_with_tracking_id') + f'/{tracking_id}'
        success_url = reverse_lazy('prof_candidate:dispute_history')
        
        return success_url

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['tracking_id'] = self.kwargs['tracking_id']

        context['pg_headline'] = 'File Dispute'
        context['app_version'] = APP_VERSION
        
        return context
        



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
        context['pg_headline'] = "My Dispute History"
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
