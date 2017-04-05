from annoying.decorators import render_to
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from core.tools import send_sms
from .forms import SendSmsForm


# Create your views here.
@login_required()
@render_to('sender/send_sms.html')
def send_sms_message(request):
    user = auth.get_user(request)
    form = SendSmsForm(request.POST or None)
    if request.POST and form.is_valid():
        data = form.cleaned_data
        r = send_sms(
            data['number_to'],
            data['message'],
            form=data['name_from'],
            priority=data['priority'],
            system_type=data['system_type']
        )
        print r
        form.save()
    return {'form': form}
