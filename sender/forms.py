from django import forms
from .models import SmsMessage


class SendSmsForm(forms.ModelForm):
    # create send sms message form
    class Meta:
        model = SmsMessage
        fields = ['name_from', 'number_to', 'message', 'priority', 'system_type']
