from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^status/$', views.get_sms_status, name='api_status'),
    url(r'^send_sms_message/$', views.send_sms_message, name='send_sms_message'),
    # url(r'^balance/$'),
    # url(r'^credit/$'),
]
