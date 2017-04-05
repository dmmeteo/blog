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
    username = models.ForeignKey('auth.User', default='auth.User')
    name_from = models.CharField(max_length=11, default='SimpleBlog')
    number_to = models.TextField(max_length=14)
    message = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    # optional fields
    priority = models.IntegerField(choices=priority_options)
    system_type = models.CharField(max_length=8, null=False)

    # response fields
    status = models.CharField(max_length=12, blank=True)
    parts = models.IntegerField(blank=True)
    cost = models.FloatField(max_length=10, blank=True)
    message_id = models.CharField(max_length=256, blank=True)
    country = models.CharField(max_length=2, blank=True)
    mccmnc = models.IntegerField(blank=True)


    # return string number_to
    def __str__(self):
        return self.number_to


