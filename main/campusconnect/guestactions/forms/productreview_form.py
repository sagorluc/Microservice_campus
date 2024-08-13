from zzz_lib.zzz_log import zzz_print
from django import forms
from django.core.exceptions import ValidationError
from ..models import mfeedback

# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# from pprint import pprint

# ******************************************************************************
class ProductReviewForm(forms.ModelForm):
    # first_name = forms.CharField(required=True)
    # email = forms.EmailField(required=True)

    # --------------------------------------------------------------------------
    class Meta:
        model = mfeedback
        fields = ("first_name", "last_name", "email_address", "product_liked", "feedback")

    # --------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(ProductReviewForm, self).__init__(*args, **kwargs)
        # self.label_suffix = ""
        #
        # # Disable display of default field help text.
        # # Don't want to disable these any more as we are now formatting display of these in template.
        # # for fieldname in ("first_name", "last_name", "email", "password1", "password2"):
        # #     self.fields[fieldname].help_text = None
        
        ### Special help text for email field.
        self.fields['email_address'].help_text = "<small style='color: grey'>We never share your email address with any 3rd party company</small>"


        ### form styling
        for visible in self.visible_fields():
            # zzz_print("    %-28s: %s" % ("visible", visible))             
            # displays html of field, ex: <input type="text" name="first_name" maxlength="150" required id="id_first_name">
        
            # make all fields required
            visible.field.required = True
        
            # Set green outline to form input
            if visible.field.widget.attrs.get('class'):
                visible.field.widget.attrs['class'] += ' form-control form-control-xs'
                visible.field.widget.attrs['style'] += ' border-color:#f1f4f8; border-radius: 0px;'
            else:
                visible.field.widget.attrs['class'] = 'form-control form-control-xs'
                visible.field.widget.attrs['style'] = 'border-color:#f1f4f8; border-radius: 0px;'

        ### form validation error msessages
        # for k, field in self.fields.items():
        #     if 'required' in field.error_messages:
        #         field.error_messages['required'] = 'This is a required field'

    # --------------------------------------------------------------------------
    def is_valid(self):
        valid = super(ProductReviewForm,self).is_valid()

        # # If a field has errors change it's border color to red.
        # for visible in self.visible_fields():
        #     if visible.errors:
        #         # zzz_print("    %-28s: %s" % ("visible", visible))
        #         if visible.field.widget.attrs.get('class'):
        #             visible.field.widget.attrs['class'] += ' form-control form-control-xs'
        #             visible.field.widget.attrs['style'] += ' border-color:red; border-radius: 0px;'
        #         else:
        #             visible.field.widget.attrs['class'] = 'form-control form-control-xs'
        #             visible.field.widget.attrs['style'] = 'border-color:red; border-radius: 0px;'

        return valid





