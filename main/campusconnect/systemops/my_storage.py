# systemops/storage_settings.py

# from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from uuid import uuid4
import string
import secrets


# class MediaStorage(S3Boto3Storage):
#     location 		= 'media'
#     default_acl 	= 'public-read'
#     file_overwrite 	= False
    
    
def gen_num_for_email():
    unique_num = str(uuid4())[:6]
    return unique_num.upper()


def generate_coupon_code(length=8):
    # Define the characters to use for the coupon code
    characters = string.ascii_uppercase + string.digits

    # Generate a random coupon code
    coupon_code = ''.join(secrets.choice(characters) for _ in range(length))

    return coupon_code