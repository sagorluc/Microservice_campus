from django import forms
from core.models.service_feedback import ServiceFeedbackModel

class ServiceFeedbackForm(forms.ModelForm):
    class Meta:
        model = ServiceFeedbackModel
        fields = ['message', 'submited_by']
        labels = {
            'message' : 'Message',
            'submited_by' : 'Submited by'
        }
        