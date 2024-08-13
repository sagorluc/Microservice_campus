from django import forms
from django.forms import Textarea
from ..models import CandidateInternalMsg


class CandidateInternalMsgForm(forms.ModelForm):
	subject = forms.CharField(
		max_length = 2000,
		label = "Write a subject line",
		widget = forms.TextInput(
			attrs = {
				'class': 'form-control'
			}
		)
	)
	msg = forms.CharField(
		max_length = 2000,
		label = "Write in details about your question",
		widget = forms.Textarea(
			attrs = {
				"rows": 5,
				"cols": 10,
				'class': 'form-control'
			}
		)
	)

	class Meta:
		model = CandidateInternalMsg
		fields = ('subject', 'msg')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.label = ''
		for visible in self.visible_fields():
			if visible.field.widget.attrs.get('class'):
				visible.field.widget.attrs['class'] += ' form-control form-control-xs'
				# visible.field.widget.attrs['style'] += ' border-color:blue; border-radius: 0px;'
			else:
				visible.field.widget.attrs['class'] = 'form-control form-control-xs'
				# visible.field.widget.attrs['style'] = 'border-color:blue; border-radius: 0px;'		

	def __str__(self):
		return "{}".format(self.id)
