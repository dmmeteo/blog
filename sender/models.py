from django.db import models
from django.utils import timezone


# Create your models here.
class SmsMessage(models.Model):
    priority_options = (
        ('', '-----'),
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High'),
    )
    username = models.ForeignKey('auth.User', default='1')
    name_from = models.CharField(max_length=11, default='SimpleBlog')
    number_to = models.CharField(max_length=14)
    message = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    dlr_timestamp = models.DateTimeField(blank=True, null=True)

    # optional fields
    priority = models.CharField(max_length=1, choices=priority_options, blank=True)
    system_type = models.CharField(max_length=8, blank=True)

    # response fields
    status = models.CharField(max_length=12, blank=True)
    parts = models.CharField(max_length=1, blank=True)
    cost = models.CharField(max_length=10, blank=True)
    message_id = models.CharField(max_length=256, blank=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    mccmnc = models.CharField(max_length=6, blank=True)

    # return string number_to
    def __str__(self):
        return self.number_to


