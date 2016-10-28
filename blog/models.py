from django.db import models
from django.utils import timezone

# Create models Post
class Post(models.Model):

	# create fields
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	# method create published_date for post
	def publish(self):
		self.published_date = timezone.now()
		self.save()

	# return string title
	def __str__(self):
		return self.title
