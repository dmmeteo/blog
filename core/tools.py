import requests
from django.conf import settings


# Here smsTool to us in senderApp
def send_sms(phone, text, **kwargs):
    data = {
        'username': settings.SMS['username'].encode('utf-8'),
        'api_key': settings.SMS['api_key'].encode('utf-8'),
        'from': settings.SMS['source'].encode('utf-8'),
        'to': phone.encode('utf-8'),
        'message': text.encode('utf-8'),
    }
    for key in kwargs:
        if kwargs[key]:
            if key == 'name_from' or key == 'number_to':
                pass
            else:
                data[key] = kwargs[key].encode('utf-8')
    r = requests.post('%(domain)s%(api_send)s' % settings.SMS, verify=False, data=data)
    return r.json().get('reply')[0] or {}
