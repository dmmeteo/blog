from django import forms
from .models import Post

# Create Post form
class PostForm(forms.ModelForm):
	# create form name & fields
	class Meta:
		model = Post
		fields = ('title', 'text')
