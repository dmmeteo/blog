from django.contrib import admin
from .models import SmsMessage


# Register your models here.
class SmsMessageAdmin(admin.ModelAdmin):
    list_display = ('number_to', 'username', 'message', 'status', 'message_id', 'created_date')
    list_filter = ['created_date', 'status']

admin.site.register(SmsMessage, SmsMessageAdmin)
