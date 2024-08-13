# from ..models import OrderFeedback
from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from guestactions.myfunctions.get_coupon_code import generate_coupon_code
from systemops.my_storage import gen_num_for_email
from mymailroom.myfunctions.send_email import send_email_customized
from ..forms import ServiceFeedbackForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
import datetime
from django.utils.html import strip_tags
from django.contrib import messages
from django.urls import reverse_lazy
import os 
from django.db import DataError
from prof_candidate.models.service_feedback import ServiceFeedbackModel
from prof_candidate.forms.service_feedback_form import ServiceFeedbackForm
from django.template.loader import render_to_string
from inventory.models import mcart


TEMPLATE_DIR = "prof_candidate/layout/my_orders/"
TEMP_DIR_EMAIL = "mymailroom/layout/prof_candidate/"
APP_VERSION = os.environ.get("VER_RESUMEWEB")

class ServiceFeedbackView(LoginRequiredMixin, CreateView):
    # import pdb; pdb.set_trace()
    template_name   = TEMPLATE_DIR + 'order-feedback.html'
    form_class      = ServiceFeedbackForm
    success_url     = reverse_lazy('prof_candidate:submit_feedback_for_order')


    def form_valid(self, form):
        try:
            query = ServiceFeedbackModel.objects.filter(created_against__tracking_id=self.kwargs["tracking_id"])
            if query.exists():
                messages.warning(self.request, "A feedback already exists for this order")
                return HttpResponseRedirect(self.request.path_info)
            
            self.object = form.save(commit=False)
            self.object.submited_by = self.request.user
            self.object.created_at = datetime.datetime.now()
            self.object.created_against = mcart.objects.get(tracking_id=self.kwargs['tracking_id'])
            self.object.save()
            messages.success(self.request, "Service Feedback Submitted")

            user_email_add = self.request.user.email
            subject = "Service Feedback " + gen_num_for_email()
            
            html_message_text = render_to_string(
                template_name=TEMP_DIR_EMAIL + 'service_feedback.html',
                context={"coupon_code_dict": generate_coupon_code()},
                using=None,
                request=None
            )
            plain_message_text = strip_tags(html_message_text)

            appname="SHOPCART"
            
            
            send_email_customized(subject, plain_message_text, html_message_text, user_email_add, appname)
            return HttpResponseRedirect(self.request.path_info)
        
        except DataError:
            return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ServiceFeedbackForm()
        context['pg_headline'] = "Order Feedback"
        context['tracking_id'] = self.kwargs['tracking_id']
        context['app_version'] = APP_VERSION
        return context

    # def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
    #     return super().post(request, *args, **kwargs)
