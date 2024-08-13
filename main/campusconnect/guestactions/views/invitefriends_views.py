import datetime
import copy
from itertools import chain
from uuid import uuid4

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.utils.html import strip_tags

from zzz_lib.zzz_log import zzz_print
from systemops.my_storage import gen_num_for_email
from guestactions.myfunctions.get_coupon_code import generate_coupon_code
from guestactions.models import InviteFriendsModel
from ..forms import InviteFriendsForm
from mymailroom.myfunctions import send_email_customized

TEMP_DIR_INVITEFRIEND   = "guestactions/invite-friends/"
TEMP_DIR_EMAIL          = 'mymailroom/layout/friends-invite/'


# ******************************************************************************
def InviteFriendsView(request):
    if request.method == "POST":
        form = InviteFriendsForm(data=request.POST)

        if form.is_valid():
            # Save necessary info in a session variable to be used in another view
            email_guest = form.cleaned_data["guest_email_address"]
            email_friend = form.cleaned_data["friend_email_address"]
            print('#'*20, email_friend, '#'*20,'line39')
            print('#'*20, email_guest, '#'*20, 'line40')
            
            # request.session["email_guest"] = email_guest
            # request.session["email_friend"] = email_friend

            if email_friend != email_guest:
                print('#'*40, 'insite if block 46')
                user_data = InviteFriendsModel.objects.add_invitefriends(
                    request             = request,
                    guest_first_name    = form.cleaned_data['guest_first_name'],
                    guest_last_name     = form.cleaned_data['guest_last_name'],
                    guest_email_address = form.cleaned_data['guest_email_address'],
                    friend_first_name   = form.cleaned_data['friend_first_name'],
                    friend_email_address= form.cleaned_data['friend_email_address'],
                    consent             = form.cleaned_data['consent']
                )
                print('#'*20, user_data, '#'*20, 'line 56')
                # Send email to user with a coupon code
                cop_code = generate_coupon_code() or "No coupon code added"
                subject = "CampusLinker Invite Friends Confirmation # " + gen_num_for_email()
                user_email_add_guest = email_guest
                appname = "GENERAL"
                email_context = {
                    'submission_id'     : str(uuid4())[:6],
                    'submission_time'   : datetime.datetime.now(),
                    'friendsemail'      : email_friend,
                    'coupon_code_dict'  : cop_code,
                }
                html_message_text = render_to_string(TEMP_DIR_EMAIL + "email_to_user.html", context=email_context)
                plain_message_text = strip_tags(html_message_text)
                send_email_customized(subject, plain_message_text, html_message_text, user_email_add_guest, appname)

                # Send email to friend with a coupon code
                cop_code = generate_coupon_code() or "No coupon code added"
                subject = "You have received an invitation from CampusLinker # " + gen_num_for_email()
                user_email_add_friend = email_friend
                email_context = {
                    'submission_id'     : str(uuid4())[:6],
                    'submission_time'   : datetime.datetime.now(),
                    'friendsemail'      : email_guest,
                    'coupon_code_dict'  : cop_code,
                }
                html_message_text = render_to_string(TEMP_DIR_EMAIL + "email_to_friend.html", context=email_context)
                plain_message_text = strip_tags(html_message_text)
                send_email_customized(subject, plain_message_text, html_message_text, user_email_add_friend, appname)

                messages.success(request, "Thank you. Confirmation messages with a coupon code have been sent to both you and your friend.")
                return redirect("guestactions:invite_friends_link")

            else:
                messages.error(request, "Opps ! You have entered same email address twice.")
                return redirect("guestactions:invite_friends_link")
        else:
            # print(form.errors)
            messages.error(request, "Sorry ! Something went wrong in your submission. Please try again.")
            return redirect("guestactions:invite_friends_link")

    else:
        form = InviteFriendsForm()

    template_name = TEMP_DIR_INVITEFRIEND + "home.html"
    context = {
        "form"          : form,
        "pg_headline"   : "Invite Friends",
        "app_version"   : settings.VER_RESUMEWEB,
        "pg_layout_type": "form_regular",
    }

    return render(request=request, template_name=template_name, context=context)



# invite friends confirmation page
# ******************************************************************************
def InviteFriendsThankyou(request):
    zzz_print("    %-28s: %s" % ("invite_friends_thankyou", "********************"))
    template_name = TEMP_DIR_INVITEFRIEND + "confirmation.html"
    email_guest = request.session.get('email_guest')
    email_friend = request.session.get('email_friend')
    
    context = {
        "email_guest": email_guest,
        "email_friend": email_friend,
        "blue": "blue",
        "red":  "red",
    }
    return render(
        request = request, 
        template_name = template_name, 
        context = context
    )
