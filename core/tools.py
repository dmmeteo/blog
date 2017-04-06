import requests
from django.conf import settings


# Here smsTool to us in senderApp
def send_sms(phone, text, **kwargs):
    data = {
        'username': settings.SMS['username'].encode('utf-8'),
        'api_key': settings.SMS['api_key'].encode('utf-8'),
        'to': phone.encode('utf-8'),
        'message': text.encode('utf-8'),
    }
    for key in kwargs:
        if kwargs[key]:
            if key == 'number_to' or key == 'message':
                pass
            elif key == 'name_from':
                data['from'] = kwargs[key].encode('utf-8')
            else:
                data[key] = kwargs[key].encode('utf-8')
    r = requests.post('%(domain)s%(api_send)s' % settings.SMS, verify=False, data=data)
    return r.json().get('reply')[0] or {}


def financial_report(*args):
    r = {}
    data = {
        'username': settings.SMS['username'].encode('utf-8'),
        'api_key': settings.SMS['api_key'].encode('utf-8'),
    }
    for arg in args:
        if arg == 'balance':
            option = 'api_balance'
        elif arg == 'credit':
            option = 'api_credit'
        r[arg] = requests.post(
            '%s%s' % (settings.SMS['domain'], settings.SMS[option]),
            verify=False,
            data=data
        ).json().get(arg)
    return r
