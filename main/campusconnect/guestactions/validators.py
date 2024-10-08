from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_email_guest(value):
    """
    Let's validate the email passed from guest user"
    """
    if not "@" in value:
        errmsg = "Sorry, the email submitted is invalid"
        raise ValidationError(errmsg)
