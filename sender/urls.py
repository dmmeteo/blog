from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^send_sms/$', views.send_sms_message, name='send_sms_message'),
    # url(r'^status/$'),
    # url(r'^balance/$'),
    # url(r'^credit/$'),
]
