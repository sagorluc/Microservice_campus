from django.conf import settings
from uuid import uuid4
import datetime
from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView
)

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
import os
from core.models import (
    CandidateInternalMsg,
)
from ..forms import CandidateInternalMsgForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags

TEMPLATE_DIR    = "prof_candidate/layout/cust_comm/"
TEMP_DIR_EMAIL  = "mymailroom/layout/prof_candidate/"
# APP_VERSION     = settings.VER_RESUMEWEB

# ******************************************************************************
class CandidateMsg(LoginRequiredMixin, CreateView):
    template_name   = TEMPLATE_DIR + "submit.html"
    form_class      = CandidateInternalMsgForm
    success_msg     = "Your message has been received successfully"
    success_url     = reverse_lazy('prof_candidate:msg_submit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_version'] = APP_VERSION
        context['pg_headline'] = "Contact us"
        return context
    
    def form_valid(self, form):
        m = form.save(commit=False)
        m.created_by = self.request.user
        m.created_at = datetime.datetime.now()
        m.save()

        # send email to the user
        appname         = "CUSTSUPP"
        subject         = "CampusLinker Confirmation # " + gen_num_for_email()
        user_email_add  = self.request.user.email
        
        email_context   = {
                'submission_id'     : str(uuid4())[:6],
                'submission_time'   : datetime.datetime.now(),
        }
        html_message_text = render_to_string(
            template_name=TEMP_DIR_EMAIL + 'cust_msg.html',
            context=email_context,
            using=None,
            request=None
        )
        plain_message_text = strip_tags(html_message_text)
        send_email_customized(subject, plain_message_text, html_message_text, user_email_add, appname)
        # email function ends

        messages.success(self.request, self.success_msg)

        return super().form_valid(form)


# ******************************************************************************
class MsgHistory(LoginRequiredMixin, ListView):
    model = CandidateInternalMsg
    template_name = TEMPLATE_DIR + "msg-history.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        zzz_print("    %-28s: %s" % ("get_context_data()", ""))

        context = super().get_context_data(**kwargs)
        context['no_of_msg'] = CandidateInternalMsg.objects.filter(created_by=self.request.user).count()
        context['app_version'] = APP_VERSION
        context['pg_headline'] = "My Message History"
        context['section_header_1'] = 'no_of_msg'

        return context

    def get_queryset(self):
        qs = CandidateInternalMsg.objects.filter(created_by=self.request.user)\
            .order_by('-created_at')
        return qs


# ******************************************************************************
class MsgDetails(LoginRequiredMixin, DetailView):
    model = CandidateInternalMsg
    template_name = TEMPLATE_DIR + "msg-details.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pg_headline'] = "My Message Details"
        context['app_version'] = APP_VERSION

        return context


# ******************************************************************************
class MsgConfirm(LoginRequiredMixin, TemplateView):
    template_name = TEMPLATE_DIR + "msg_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_version'] = APP_VERSION

        return context
