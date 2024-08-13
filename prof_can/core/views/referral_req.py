from zzz_lib.zzz_log import zzz_print
import json
from uuid import uuid4
from django.shortcuts import render
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
from django.contrib import messages
# from datetime import datetime
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import (
    ListView,
    UpdateView,
    DetailView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic.edit import CreateView

TEMPLATE_DIR = "prof_candidate/layout/referral/"
######################################

class RefProgSubmitReqByCand(LoginRequiredMixin, TemplateView):
	template_name = TEMPLATE_DIR + "submit-req.html"


