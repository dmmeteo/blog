from django import forms
from .models import *

# Create Post form
class PostForm(forms.ModelForm):
	# create form name & fields
	class Meta:
		model = Post
		fields = ('title', 'text')

class CommentForm(forms.ModelForm):
	# create form comments
	class Meta:
		model = Comment
		fields = ('author', 'email', 'text')
