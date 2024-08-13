from django import forms
from ..models import OrderFeedbackModel


class OrderFeedbackForm(forms.ModelForm):    
    class Meta:
        model   = OrderFeedbackModel
        fields  = '__all__'
        exclude = ('created_at', 'created_against', 'submited_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
