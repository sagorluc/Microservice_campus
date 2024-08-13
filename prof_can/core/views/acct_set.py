import json
from uuid import uuid4
from django.shortcuts import render
from django.utils.html import strip_tags
from base64 import b64decode, b64encode
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import connection
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.utils import timezone
from django.views.generic.edit import FormView
from django.contrib import messages
from django.template.loader import (
    render_to_string,
    get_template
)
import os
from django.views.generic import (
    ListView,
    UpdateView,
    DetailView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import (
    AccDeactivateForm,
    PasswordUpdateForm,
)
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from core.models import (DeactivatedAccountModel,)
from django.contrib.auth import update_session_auth_hash

import datetime
from django.conf import settings 

TEMPLATE_DIR    = "prof_candidate/layout/acct_settings/"
TEMP_DIR_EMAIL  = "mymailroom/layout/mmhauth/"
# APP_VERSION     = settings.VER_RESUMEWEB



## Basic Info page
class AcctSettingsHomeView(LoginRequiredMixin, TemplateView):
    template_name = TEMPLATE_DIR + "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pg_headline'] = 'Account Basic Information'
        context['app_version'] = APP_VERSION
        
        return context


## password change form submission
class UpdatePassView(LoginRequiredMixin, PasswordChangeView):
    template_name   = TEMPLATE_DIR + "update_pass.html"
    form_class      = PasswordUpdateForm
    success_url     = reverse_lazy('mmhauth:mmh_auth_login_request')

    def form_valid(self, form):
        form.save()
        form.user = self.request.user

        # send email to the user
        appname         = "AUTH"
        subject         = "CampusLinker Password Update Confirmation # " + gen_num_for_email()
        user_email_add  = self.request.user.email
        
        email_context   = {
                'submission_id'     : str(uuid4())[:6],
                'submission_time'   : datetime.datetime.now(),
        }
        html_message_text = render_to_string(
            template_name=TEMP_DIR_EMAIL + 'update_pass.html',
            context=email_context,
            using=None,
            request=None
        )
        plain_message_text = strip_tags(html_message_text)
        send_email_customized(subject, plain_message_text, html_message_text, user_email_add, appname)
        # email function ends

        update_session_auth_hash(self.request, form.user)
        logout(self.request)

        messages.success(self.request, "Password Updated Successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pg_headline'] = 'Update Your Password'
        context['app_version']  = APP_VERSION

        return context


## Account Deactivation form submission
class SubmitAccountDeactivateView(LoginRequiredMixin, CreateView):
    template_name   = TEMPLATE_DIR + "acct_deactivate.html"
    form_class      = AccDeactivateForm
    model           = DeactivatedAccountModel
    success_url     = reverse_lazy('mmhauth:mmh_auth_login_request')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.email = self.request.user.email
        self.object.save()

        # send email to the user
        appname         = "AUTH"
        subject         = "CampusLinker Account Deactivation Confirmation # " + gen_num_for_email()
        user_email_add  = self.request.user.email
        
        email_context   = {
                'submission_id'     : str(uuid4())[:6],
                'submission_time'   : datetime.datetime.now(),
        }
        html_message_text = render_to_string(
            template_name=TEMP_DIR_EMAIL + 'account_deactivate.html',
            context=email_context,
            using=None,
            request=None
        )
        plain_message_text = strip_tags(html_message_text)
        send_email_customized(subject, plain_message_text, html_message_text, user_email_add, appname)
        # email function ends
        
        logout(self.request)

        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)

        kwargs['email'] = self.request.user.email

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pg_headline'] = 'Account Deactivation Form'
        context['app_version'] = APP_VERSION

        return context


# Account Deactivation Confirm View
##***************************************************
class AccDeactivateConfirmView(LoginRequiredMixin, TemplateView):
    template_name = TEMPLATE_DIR+"acct_deactivate_done.html"

