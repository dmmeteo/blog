from django import forms
from .models import Post, Comment

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
		widgets = {
					'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
					'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
					'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comment'}),
				}
