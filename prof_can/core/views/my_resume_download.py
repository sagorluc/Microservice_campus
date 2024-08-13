# Standard Library Imports
import os
import datetime
import copy
from decimal import Decimal
from pprint import pprint

# Third-party Library Imports
import boto3

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


# Constants
APP_VERSION = os.environ.get("VER_RESUMEWEB")


# ******************************************************************************
def resume_download_view(request, bucket_name, object_name):
    # Set the AWS credentials
    ACCESS_KEY  = os.environ.get('AWS_ACCESS_KEY_ID')
    SECRET_KEY  = os.environ.get('AWS_SECRET_ACCESS_KEY')

    bucket_name = os.environ.get('AWS_S3_MASTER_BUCKET_NAME')
    folder_name = settings.AWS_S3_MACRT_RESUME_FOLDER

    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(bucket_name)
    objects = my_bucket.objects.filter(Prefix= folder_name + '/')
    for obj in objects:
        path, filename = os.path.split(obj.key)
        my_bucket.download_my_file(obj.key, filename)

    return HttpResponse("Download successful")

