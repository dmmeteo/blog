from django.db import models
from django.utils import timezone

# Create model Category
class Category(models.Model):
	# create fields
	title = models.CharField(max_length=200)
	discript = models.TextField(blank=True, null=True)
	# file = FileField()

	# return string title
	def __str__(self):
		return self.title

# Create models Post
class Post(models.Model):
	# create fields
	author = models.ForeignKey('auth.User', default='auth.User')
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=200)
	text = models.TextField()
	likes = models.IntegerField(default=0)
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	# method create published_date for post
	def publish(self):
		self.published_date = timezone.now()
		self.save()

	# return string title
	def __str__(self):
		return self.title

# Create model Comments
class Comment(models.Model):
	# crete fields
	author = models.CharField(max_length=200)
	text = models.TextField()
	email = models.EmailField()
	post = models.ForeignKey(Post)
	created_date = models.DateTimeField(default=timezone.now)

	# return string text
	def __str__(self):
		return self.text

