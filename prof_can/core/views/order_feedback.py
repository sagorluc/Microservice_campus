from uuid import uuid4
from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from ..forms import OrderFeedbackForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
import datetime
from django.utils.html import strip_tags
from django.contrib import messages
from django.urls import reverse_lazy
import os 
from django.db import DataError
from core.models import OrderFeedbackModel
from django.template.loader import render_to_string
from django.conf import settings

TEMPLATE_DIR    = "prof_candidate/layout/order-feedback/"
TEMP_DIR_EMAIL  = "mymailroom/layout/prof_candidate/"
# APP_VERSION     = settings.VER_RESUMEWEB

class OrderFeedbackSubmitView(LoginRequiredMixin, CreateView):
    template_name   = TEMPLATE_DIR + 'order-feedback.html'
    form_class      = OrderFeedbackForm
    success_url     = reverse_lazy('prof_candidate:dashboard_homepage')
    success_msg     = 'Your feedback has been submitted successfully'

    def form_valid(self, form):
        try:
            query = OrderFeedbackModel.objects.filter(created_against__tracking_id=self.kwargs["tracking_id"])
            if query.exists():
                messages.warning(self.request, "You have already submitted a feedback for this order")
                return HttpResponseRedirect(self.request.path_info)
            
            self.object = form.save(commit=False)
            self.object.submited_by = self.request.user.email
            self.object.created_at = datetime.datetime.now()
            self.object.created_against = mcart.objects.get(tracking_id=self.kwargs['tracking_id'])
            self.object.save()

            # generate/select a coupon code from coupon table
            cop_code_dict   = generate_coupon_code()

            # send email to the user
            appname         = "CUSTSUPP"
            subject         = "CampusLinker Service Feedback Confirmation # " + gen_num_for_email()
            user_email_add  = self.request.user.email
            
            email_context   = {
                'submission_id'     : str(uuid4())[:6],
                'submission_time'   : datetime.datetime.now(),
                'coupon_code_dict'  : cop_code_dict,
            }
            html_message_text = render_to_string(
                template_name=TEMP_DIR_EMAIL + 'order_feedback.html',
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['form'] = OrderFeedbackForm()
        context['tracking_id'] = self.kwargs['tracking_id']

        context['app_version'] = APP_VERSION
        context['pg_headline'] = "Order Feedback"
        
        return context
