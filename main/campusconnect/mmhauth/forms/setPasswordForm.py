from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.utils.translation import gettext_lazy  as _

from zzz_lib.zzz_log import zzz_print


# ******************************************************************************
class SetPasswordCustomForm(SetPasswordForm):
    # new_password1 = forms.CharField(
    #     label=mark_safe("<strong>Password</strong>"),
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    #     help_text=None #password_validation.password_validators_help_text_html(),
    # )
    # new_password2 = forms.CharField(
    #     label=mark_safe("<strong>Password Confirmation</strong>"),
    #     widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    #     strip=False,
    #     help_text=_("<small style='color: grey'>Enter the same password as above, for verification</small>"),
    # )

    # error_messages = {
    #     'password_mismatch': _("The two password fields didn't match."),
    # }
    class Meta:
        # model = User
        fields = ("new_password1", "new_password2")

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(SetPasswordCustomForm, self).__init__(user, *args, **kwargs)
        self.label_suffix = ""

        for visible in self.visible_fields():
            if visible.field.widget.attrs.get('class'):
                visible.field.widget.attrs['class'] += ' form-control form-control-xs'
                visible.field.widget.attrs['style'] += ' border-color:#D9D9D9; border-radius: 0px;'
            else:
                visible.field.widget.attrs['class'] = 'form-control form-control-xs'
                visible.field.widget.attrs['style'] = 'border-color:#D9D9D9; border-radius: 0px;'
