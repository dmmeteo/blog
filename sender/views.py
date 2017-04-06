from annoying.decorators import render_to
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from core.tools import send_sms, financial_report
from .models import SmsMessage
from .forms import SendSmsForm


# Create your views here.
def get_sms_status(request):
    if request.GET:
        # msg = SmsMessage.objects.get(message_id=request.GET['msgid'])
        msg = get_object_or_404(SmsMessage, message_id=request.GET['msgid'])
        msg.status = request.GET['status']
        msg.dlr_timestamp = request.GET['dlr_timestamp']
        msg.save()
        return HttpResponse('ok', content_type='text/html')


@login_required()
@render_to('sender/send_sms.html')
def send_sms_message(request):
    report = financial_report('balance', 'credit')
    form = SendSmsForm(request.POST or None)
    if request.POST and form.is_valid():
        data = form.cleaned_data
        # response = {
        #     u'status': u'OK',
        #     u'cost': u'0.005355',
        #     u'country': None,
        #     u'number': u'380502707832',
        #     u'mccmnc': u'25501',
        #     u'parts': 1,
        #     u'message_id': u'f3e5db0a-0d28-42ed-9392-782648996ff8'
        # }
        response = send_sms(
            data['number_to'],
            data['message'],
            form=data['name_from'],
            priority=data['priority'],
            system_type=data['system_type']
        )
        msg = form.save(commit=False)
        msg.username = request.user
        msg.status = response['status']
        msg.cost = response['cost']
        msg.country = response['country']
        msg.number = response['number']
        msg.mccmnc = response['mccmnc']
        msg.parts = response['parts']
        msg.message_id = response['message_id']
        msg.save()

    return {'form': form, 'report': report}




