from uuid import uuid4
import datetime
import copy
from django.contrib import messages
from decimal import Decimal
from pprint import pprint
import os
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView  # , UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.utils.html import strip_tags
from core.models.order_cancellation import OrderCancellationRequest

from ..forms import OrderCancellationRequestForm
TEMPLATE_DIR    = "prof_candidate/layout/order_cancellation/"
TEMP_DIR_EMAIL  = "mymailroom/layout/prof_candidate/"
APP_VERSION     = os.environ.get("VER_RESUMEWEB")

from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
# ******************************************************************************
class OrderCancellationRequestView(LoginRequiredMixin, CreateView):
    template_name   = TEMPLATE_DIR + 'submit.html'
    form_class      = OrderCancellationRequestForm
    model           = OrderCancellationRequest
    success_url     = reverse_lazy('prof_candidate:order_history_all') 
    success_msg     = "Your order has been cancelled successfully"

    def form_valid(self, form, **kwargs):
        query = OrderCancellationRequest.objects.filter(created_for=self.kwargs['tracking_id'])
        if query.exists():
            messages.warning(self.request, "Order is already cancelled ")
            return HttpResponseRedirect(self.request.path_info)
        self.object = form.save(commit=False)
        self.object.created_at = datetime.datetime.now()
        self.object.created_for = self.kwargs.get('tracking_id')
        self.object.submitted_by = self.request.user.email
        self.object.save()

        qs = mcart.objects.mcartInstance_userOrderHistory_byTrackingId(self.request, tracking_id=self.object.created_for)
        zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))

        mcart_instance = qs[0]
        mcart_instance.processing_status = "cancelled"
        mcart_instance.save()

        # generate/select a coupon code from coupon table
        cop_code_dict   = generate_coupon_code()

        # send email to the user
        appname         = "CUSTSUPP"
        subject         = "CampusLinker Order Cancellation Confirmation # " + gen_num_for_email()
        user_email_add  = self.request.user.email
        
        email_context   = {
                'submission_id'     : str(uuid4())[:6],
                'submission_time'   : datetime.datetime.now(),
                'coupon_code_dict'  : cop_code_dict,
        }
        html_message_text = render_to_string(
            template_name=TEMP_DIR_EMAIL + 'order_cancellation.html',
            context=email_context,
            using=None,
            request=None
        )
        plain_message_text = strip_tags(html_message_text)
        send_email_customized(subject, plain_message_text, html_message_text, user_email_add, appname)
        # email function ends

        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OrderCancellationRequestView, self).get_context_data(**kwargs)
        context['header_text'] = "Order Cancellation Form"
        # get relevant order details
        # context['qs'] = mcart.objects.mcartInstance_userOrderHistory_byTrackingId(id=kwargs['tracking_id'])
        context['tracking_id'] = self.kwargs.get('tracking_id')
        context['app_version'] = APP_VERSION
        context['pg_headline'] = "Order Cancellation Request"
        return context


# ******************************************************************************
class CancellationDetailsView(LoginRequiredMixin, DetailView):
    template_name   = TEMPLATE_DIR + 'details.html'
    model           = OrderCancellationRequest

    def get_object(self, queryset=None):
        # return MyModel.objects.get(pk=self.kwargs['pk'])
        return OrderCancellationRequest.objects.filter(created_for=self.kwargs['tracking_id'])

    def get_context_data(self, **kwargs):
        context = super(CancellationDetailsView, self).get_context_data(**kwargs)

        # get relevant order details
        # qs = OrderCancellationRequest.objects.filter(created_for=self.kwargs.get('tracking_id'))
        # context['qs'] = qs

        context['section_header_1'] = "Order Cancellation Information"
        context['app_version'] = APP_VERSION
        return context



# ******************************************************************************
def OrderCancelHistoryAll(request):
    zzz_print("    %-28s: %s" % ("OrderCancelHistoryAll", "********************"))
    template = loader.get_template(TEMPLATE_DIR + "cancel_history.html")
    qs = mcart.objects.filter(processing_status="cancelled", muser=request.user)
    # zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))
    print(f"qs: ###########: {qs}")
    context = {
        "no_of_orders": qs.count(),
        "object_list": qs,
        "app_version": APP_VERSION,
        "pg_headline": "Order Cancellation History",
    }
    return HttpResponse(template.render(context, request))

### ******************************************************************************
# class CancellationDetailsView(LoginRequiredMixin, DetailView):
#     template_name   = TEMPLATE_DIR + 'details.html'
#     model           = OrderCancellationRequest

#     def get_context_data(self, **kwargs):
#         context = super(CancellationDetailsView, self).get_context_data(**kwargs)

#         # get relevant order details
#         qs = OrderCancellationRequest.objects.filter(created_for=self.kwargs.get('tracking_id'))
#         context['qs'] = qs

#         context['header_text'] = "Order Cancellation Message"
#         context['app_version'] = APP_VERSION
#         return context


# ******************************************************************************
class OrderCancellationConfirmationView(LoginRequiredMixin, DetailView):
    template_name   = TEMPLATE_DIR + 'confirmation.html'
    model           = OrderCancellationRequest

    def get_context_data(self, **kwargs):
        context = super(OrderCancellationConfirmationView, self).get_context_data(**kwargs)
        context['header_text'] = "Order Cancellation Message"
        # get relevant order details
        qs = OrderCancellationRequest.objects.filter(created_for=self.kwargs.get('tracking_id'))
        context['qs'] = qs
        context['app_version'] = APP_VERSION
        return context



# ******************************************************************************
def CancelOrder_mmh(request, tracking_id):
    zzz_print("    %-28s: %s" % ("CancelOrder_mmh", tracking_id))

    qs = mcart.objects.mcartInstance_userOrderHistory_byTrackingId(request, tracking_id)
    zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))

    # FATAL ERROR:
    # MMH: CHANGE THIS TO CAPTURING ERROR MESSAGE AND REDIRECTING TO AN ERROR VIEW PAGE WHERE THIS MESSAGE IS DISPLAYED AND LOGGED
    if qs.count() != 1:
        zzz_print_exit("    %-28s: %s" % ("qs.count() != 1", qs.count()))

    mcart_instance = qs[0]

    # FATAL ERROR:
    # MMH: CHANGE THIS TO CAPTURING ERROR MESSAGE AND REDIRECTING TO AN ERROR VIEW PAGE WHERE THIS MESSAGE IS DISPLAYED AND LOGGED
    if mcart_instance.grace_left_in_seconds() < 1:
        zzz_print_exit("    %-28s: %s" % ("grace_left_in_seconds < 1",
                       mcart_instance.grace_left_in_seconds()))

    # FATAL ERROR:
    # MMH: CHANGE THIS TO CAPTURING ERROR MESSAGE AND REDIRECTING TO AN ERROR VIEW PAGE WHERE THIS MESSAGE IS DISPLAYED AND LOGGED
    if mcart_instance.processing_status == "delivered":
        zzz_print_exit("    %-28s: %s" % ("mcart_instance.processing_status",
                       mcart_instance.processing_status))
    if mcart_instance.processing_status == "cancelled":
        zzz_print_exit("    %-28s: %s" % ("mcart_instance.processing_status",
                       mcart_instance.processing_status))
    if mcart_instance.processing_status == "error":
        zzz_print_exit("    %-28s: %s" % ("mcart_instance.processing_status",
                       mcart_instance.processing_status))

    zzz_print("    %-28s: %s" % ("request.method", request.method))
    if request.method == 'POST':
        form = form_mcompleted_refund(request.POST, request.FILES)
        if form.is_valid():
            reason = form.cleaned_data.get('reason')
            explanation = form.cleaned_data.get('explanation')
            zzz_print("    %-28s: %s" % ("reason", reason))
            zzz_print("    %-28s: %s" % ("explanation", explanation))

            capture_id = mcart_instance.mcompleted_purchase.capture_id
            zzz_print("    %-28s: %s" % ("capture_id", capture_id))

            if not capture_id:
                zzz_print("    %-28s: %s" % ("CAPTURE_ID",
                          "NOT SET. ARE YOU USING OLD PURCHASES???"))
                zzz_print("    %-28s: %s" % ("CAPTURE_ID",
                          "NOT SET. ARE YOU USING OLD PURCHASES???"))
                zzz_print("    %-28s: %s" % ("CAPTURE_ID",
                          "NOT SET. ARE YOU USING OLD PURCHASES???"))
                zzz_print("    %-28s: %s" % ("CAPTURE_ID",
                          "NOT SET. ARE YOU USING OLD PURCHASES???"))
                zzz_print_exit("    %-28s: %s" % ("CAPTURE_ID",
                               "NOT SET. ARE YOU USING OLD PURCHASES???"))

            mcart_qs = mcart.objects.filter(id=mcart_instance.id)
            zzz_print("    %-28s: %s" % ("mcart_qs.count()", mcart_qs.count()))

            cart_context = cart_context_forQuerySet(request, mcart_qs)
            
            
            ########################################################
            ###### Remove some code about order cancellation #######
            ########################################################

            to_emails_list = copy.deepcopy(settings.DEVELOPMENT_ONLY_EMAIL_RECIPIENTS)
            if request.user.is_authenticated:
                to_emails_list.append(request.user.email)
            elif 'mmh_guestemailaddress' in request.session:
                to_emails_list.append(request.session['mmh_guestemailaddress'])
            elif mcart_instance.mcompleted_purchase.guest_login_email_address:
                to_emails_list.append(
                    mcart_instance.mcompleted_purchase.guest_login_email_address)
            else:
                zzz_print("    %-28s: %s" % ("WARNING", "(NOT request.user.is_authenticated) AND (mmh_guestemailaddress NOT in request.session) and (NOT IN mcart_instance.mcompleted_purchase.guest_login_email_address)"))

            if data and data['status'] == 'COMPLETED':
                # zzz_print("    %-28s: %s" % ("refund data['id']", data['id']))
                mcart_instance.set_processing_status_cancelled()

                # create mcompleted_refund instance
                icompleted_refund = mcompleted_refund.objects.add_mcompleted_refund(
                    refund_id=data['id'],
                    amount_currencycode=data['amount']['currency_code'],
                    amount_value=Decimal(data['amount']['value']),
                    reason=reason,
                    explanation=explanation
                )

                
                # and update mcart_instance foreign key for this new mcompleted_refund instance
                mcart_instance.mcompleted_refund = icompleted_refund
                mcart_instance.save()

                # SEND AN EMAIL CONFIRMING REFUND APPROVED.
                plain_message_text = "About the cancellation: \n" + os.linesep
                # plain_message_text  += "date: "+ str(datetime.datetime.now())+"\n"
                plain_message_text += "Amount: $" + \
                    data['amount']['value'] + "\n" + os.linesep
                plain_message_text += "Refund Reference Id: " + \
                    data['id']+"\n" + os.linesep
                plain_message_text += "About the original order: " + \
                    mcart_instance.title + "." + os.linesep
                change_notice = plain_message_text
                email_address = request.user.email
                subject = "Order cancelled successfully" + gen_num_for_email()
                time = datetime.datetime.now()
                send_email_customized(email_address, subject, change_notice, time)

                return HttpResponseRedirect(
                    reverse('prof_candidate:mmh_cancel_order_success', kwargs={
                            'tracking_id': mcart_instance.tracking_id})
                )
            else:  # refund failed
                mcart_instance.set_processing_status_error()

                # SEND AN EMAIL INDICATING REFUND FAILED
                plain_message_text = "A refund of " + \
                    data['amount']['value'] + " was NOT, REPEAT NOT, successfully processed for the cancellation of " + \
                    mcart_instance.title + "."
                plain_message_text += "Refund Reference Id = " + \
                    data['id'] + "."
                plain_message_text += " This email text and its html version need work."
                html_message_text = plain_message_text
                return HttpResponseRedirect(
                    reverse('prof_candidate:mmh_cancel_order_failed', kwargs={
                            'tracking_id': mcart_instance.tracking_id})
                )
        else:
            zzz_print("    %-28s: %s" % ("form.is NOT valid()", ""))
    else:
        form = form_mcompleted_refund()

    context_data = {'form': form}
    form_html = render_to_string(
        template_name = "prof_candidate/pg-contents/order_cancellation/form.html", 
        context=context_data, request=request
    )
    
    template = loader.get_template(TEMPLATE_DIR + "order_cancel.html")
    context = {
        "header_text": "Cancelling Order",
        "object": mcart_instance,
        "form": form_html,
        "app_version" : APP_VERSION
       
    }
    return HttpResponse(template.render(context, request))


# ******************************************************************************
def CancelOrderSuccess_mmh(request, tracking_id):
    zzz_print("    %-28s: %s" % ("CancelOrderSuccess_mmh", tracking_id))

    qs = mcart.objects.mcartInstance_userOrderHistory_byTrackingId(request, tracking_id)
    zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))
    mcart_instance = qs[0]

    template = loader.get_template(TEMPLATE_DIR + "order_cancel.html")
    context = {
        "header_text": "Order Cancelled",
        "object": mcart_instance,
        "form": "",
        "app_version": APP_VERSION
        
    }
    return HttpResponse(template.render(context, request))

